from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import status
from app.ai.interfaces import ai_recommendation_provider
from app.core.config import settings
from app.core.exceptions import AppError
from app.domain.enums import AssessmentStatus, EvidenceType, SkillGapPriority
from app.repositories.in_memory import db


class SkillGapService:
    @staticmethod
    def calculate_gaps_for_user(user_id: str) -> List[Dict[str, Any]]:
        gaps: List[Dict[str, Any]] = []
        for comp in db.competencies.values():
            delta = comp["required_level"] - comp["current_level"]
            if delta > 0:
                priority = SkillGapPriority.HIGH if delta >= 2 else SkillGapPriority.MEDIUM
                comp_evidence = [
                    e for e in db.evidence if e["user_id"] == user_id and e["competency_id"] == comp["id"]
                ]
                gaps.append(
                    {
                        "competency_id": comp["id"],
                        "competency_name": comp["name"],
                        "domain": comp["domain"],
                        "current_level": comp["current_level"],
                        "required_level": comp["required_level"],
                        "gap": delta,
                        "priority": priority,
                        "confidence": comp["confidence"],
                        "why_it_matters": comp["why_it_matters"],
                        "evidence": comp_evidence,
                    }
                )
        gaps.sort(key=lambda g: g["gap"], reverse=True)
        return gaps


class RecommendationService:
    @staticmethod
    async def get_or_generate_for_user(user_id: str) -> List[Dict[str, Any]]:
        gaps = SkillGapService.calculate_gaps_for_user(user_id)
        return await ai_recommendation_provider.generate_recommendations(user_id, gaps)


class CompetencyUpdateService:
    @staticmethod
    def record_assessment_outcome(
        user_id: str,
        competency_id: str,
        assessment_id: str,
        score_percent: float,
        request_id: str,
    ) -> Dict[str, Any] | None:
        if competency_id not in db.competencies:
            return None

        comp = db.competencies[competency_id]
        prev_level = comp["current_level"]
        new_level = prev_level
        if score_percent >= settings.LEVEL_UPGRADE_SCORE_THRESHOLD and prev_level < 5:
            new_level = prev_level + 1

        ev_id = f"ev-asmt-{len(db.evidence) + 101}"
        new_ev = {
            "id": ev_id,
            "user_id": user_id,
            "competency_id": competency_id,
            "source": f"Assessment {assessment_id}",
            "title": f"Verified Assessment Completion ({score_percent:.1f}%)",
            "type": EvidenceType.ASSESSMENT,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "score": score_percent,
            "confidence": 0.93,
            "metadata": {"previous_level": prev_level, "new_level": new_level},
        }
        db.evidence.append(new_ev)

        comp["current_level"] = new_level
        comp["confidence"] = 0.93

        history_entry = {
            "id": f"hist-{len(db.competency_history) + 1:03d}",
            "user_id": user_id,
            "competency_id": competency_id,
            "previous_level": prev_level,
            "new_level": new_level,
            "evidence_id": ev_id,
            "confidence": 0.93,
            "calculated_at": datetime.now(timezone.utc).isoformat(),
        }
        db.competency_history.append(history_entry)

        if new_level > prev_level and user_id in db.users:
            db.users[user_id]["overall_competency_score"] = min(
                100, db.users[user_id]["overall_competency_score"] + 9
            )

        db.log_audit(
            user_id=user_id,
            action="COMPETENCY_UPDATE",
            resource=competency_id,
            result="SUCCESS",
            request_id=request_id,
            metadata={"previous_level": prev_level, "new_level": new_level, "score": score_percent},
        )
        return history_entry


class AssessmentService:
    @staticmethod
    def submit_assessment(
        assessment_id: str,
        user_id: str,
        answers: Dict[str, str],
        request_id: str,
    ) -> Dict[str, Any]:
        if assessment_id not in db.assessments:
            raise AppError("NOT_FOUND", "Assessment not found", status.HTTP_404_NOT_FOUND)

        asmt = db.assessments[assessment_id]
        questions = asmt["questions"]
        if not questions:
            raise AppError("EMPTY_ASSESSMENT", "Assessment has no questions", status.HTTP_400_BAD_REQUEST)

        correct = 0
        valid_options = {"A", "B", "C", "D"}
        for q in questions:
            qid = q["id"]
            if qid in answers:
                submitted_opt = answers[qid]
                if submitted_opt not in valid_options:
                    raise AppError(
                        "INVALID_OPTION",
                        f"Option '{submitted_opt}' is not valid for question {qid}",
                        status.HTTP_400_BAD_REQUEST,
                    )
                if submitted_opt == q["correct_option"]:
                    correct += 1

        total = len(questions)
        score_percent = round((correct / total) * 100.0, 2)
        asmt["status"] = AssessmentStatus.COMPLETED

        update_record = CompetencyUpdateService.record_assessment_outcome(
            user_id=user_id,
            competency_id=asmt["competency_id"],
            assessment_id=assessment_id,
            score_percent=score_percent,
            request_id=request_id,
        )

        result_payload = {
            "assessment_id": assessment_id,
            "user_id": user_id,
            "status": AssessmentStatus.COMPLETED,
            "score_percent": score_percent,
            "correct_answers": correct,
            "incorrect_answers": total - correct,
            "total_questions": total,
            "competency_update": update_record,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
        asmt["latest_result"] = result_payload

        db.log_audit(
            user_id=user_id,
            action="ASSESSMENT_SUBMIT",
            resource=assessment_id,
            result="SUCCESS",
            request_id=request_id,
            metadata={"score_percent": score_percent},
        )
        return result_payload
