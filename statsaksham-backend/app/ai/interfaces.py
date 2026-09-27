from typing import Any, Dict, List


class AIRecommendationProvider:
    """Pluggable interface for Part 6-8 Embedding / Hybrid Recommendation Engine."""

    async def generate_recommendations(
        self, user_id: str, skill_gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        recommendations = []
        for idx, gap in enumerate(skill_gaps, start=1):
            recommendations.append(
                {
                    "id": f"rec-{gap['competency_id']}",
                    "step_number": idx,
                    "item": f"Targeted Mastery Module: {gap['competency_name']}",
                    "type": "IGOT_COURSE" if idx % 2 == 1 else "NSSTA_PROGRAMME",
                    "competency_id": gap["competency_id"],
                    "competency_name": gap["competency_name"],
                    "priority": gap["priority"],
                    "status": "RECOMMENDED",
                    "estimated_duration": "4 hours",
                    "reason": (
                        f"Recommended because your role requires Level {gap['required_level']} "
                        f"in {gap['competency_name']} and your current verified level is Level {gap['current_level']}."
                    ),
                    "competency_match": 0.94,
                    "role_relevance": 0.96,
                    "difficulty_fit": 0.90,
                    "confidence": 0.92,
                    "evidence": gap.get("evidence", []),
                }
            )
        return recommendations


class AIAssessmentProvider:
    """Pluggable interface for Part 6-8 RAG / Document MCQ Generation Engine."""

    async def generate_questions_from_document(self, document_id: str) -> List[Dict[str, Any]]:
        return []


class AITutorProvider:
    """Pluggable interface for Part 6-8 Grounded Official Statistics AI Assistant."""

    async def answer_query(self, user_id: str, query: str) -> Dict[str, Any]:
        return {
            "answer": "Grounded response stub ready for RAG integration.",
            "disclaimer": "AI-generated responses should be verified against source materials.",
        }


ai_recommendation_provider = AIRecommendationProvider()
ai_assessment_provider = AIAssessmentProvider()
ai_tutor_provider = AITutorProvider()
