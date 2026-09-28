import os
import time
from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, File, Query, Request, UploadFile, status
from pydantic import BaseModel, EmailStr, Field
from app.api.dependencies import get_current_user, get_request_id, require_roles
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.enums import DocumentStatus, LearningStatus, QuestionStatus, Role
from app.integrations.base import igot_adapter, nssta_adapter, tpac_adapter
from app.repositories.in_memory import db
from app.services.quiz_generator import QuizGenerationError, generate_quiz
from app.services.business_services import (
    AssessmentService,
    RecommendationService,
    SkillGapService,
)

api_router = APIRouter()

_quiz_calls: list = []  # timestamps of recent generations (simple in-memory rate limit)
QUIZ_MAX_PER_HOUR = int(os.getenv("QUIZ_MAX_PER_HOUR", "20"))


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class QuizGenerateRequest(BaseModel):
    text: str = Field(min_length=100, max_length=60000)
    num_questions: int = Field(default=5, ge=1, le=15)
    difficulty: str = Field(default="Medium", max_length=20)
    competency: str = Field(default="General", max_length=120)
    title: str = Field(default="Uploaded learning material", max_length=200)


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class UserProfilePatch(BaseModel):
    current_assignment: str | None = None
    languages: list[str] | None = None


class EnrollmentCreateRequest(BaseModel):
    course_id: str


class AssessmentSubmitRequest(BaseModel):
    answers: Dict[str, str]


@api_router.get("/health", summary="System Health Summary", tags=["Health"])
async def health_check(req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    return {
        "data": {
            "status": "healthy",
            "services": {
                "application": "healthy",
                "database": "ready",
                "igot": "mock",
                "ai": "ready",
            },
        },
        "meta": {"env": settings.APP_ENV},
        "request_id": req_id,
    }


@api_router.get("/health/live", summary="Liveness Probe", tags=["Health"])
async def health_live(req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    return {"data": {"alive": True}, "meta": {}, "request_id": req_id}


@api_router.get("/health/ready", summary="Readiness Probe", tags=["Health"])
async def health_ready(req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    return {"data": {"ready": True}, "meta": {}, "request_id": req_id}


@api_router.post("/auth/login", summary="Authenticate User", tags=["Auth"])
async def login(payload: LoginRequest, req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    matched_user = next(
        (u for u in db.users.values() if u["email"].lower() == payload.email.lower()),
        None,
    )
    if not matched_user or not verify_password(payload.password, matched_user["password_hash"]):
        raise AppError(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    token = create_access_token(
        subject=matched_user["id"],
        role=matched_user["role"],
        department_id=matched_user["department_id"],
    )
    db.log_audit(matched_user["id"], "AUTH_LOGIN", "auth", "SUCCESS", req_id)
    user_safe = {k: v for k, v in matched_user.items() if k != "password_hash"}
    return {
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": user_safe,
        },
        "meta": {},
        "request_id": req_id,
    }


@api_router.get("/auth/me", summary="Get Current Authenticated Identity", tags=["Auth"])
async def auth_me(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    user_safe = {k: v for k, v in current_user.items() if k != "password_hash"}
    return {"data": user_safe, "meta": {}, "request_id": req_id}


@api_router.post("/auth/logout", summary="Logout Session", tags=["Auth"])
async def auth_logout(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    db.log_audit(current_user["id"], "AUTH_LOGOUT", "auth", "SUCCESS", req_id)
    return {"data": {"logged_out": True}, "meta": {}, "request_id": req_id}


@api_router.get("/users/me", summary="Get My Official Profile", tags=["Users"])
async def get_my_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    user_safe = {k: v for k, v in current_user.items() if k != "password_hash"}
    return {"data": user_safe, "meta": {}, "request_id": req_id}


@api_router.patch("/users/me", summary="Update My Profile", tags=["Users"])
async def update_my_profile(
    patch: UserProfilePatch,
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    if patch.current_assignment is not None:
        current_user["current_assignment"] = patch.current_assignment
    if patch.languages is not None:
        current_user["languages"] = patch.languages
    db.log_audit(current_user["id"], "PROFILE_UPDATE", current_user["id"], "SUCCESS", req_id)
    user_safe = {k: v for k, v in current_user.items() if k != "password_hash"}
    return {"data": user_safe, "meta": {}, "request_id": req_id}


@api_router.get("/users", summary="List Officials (Admin Only)", tags=["Users"])
async def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(require_roles([Role.ADMIN, Role.SUPER_ADMIN])),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    all_users = [{k: v for k, v in u.items() if k != "password_hash"} for u in db.users.values()]
    start = (page - 1) * page_size
    return {
        "data": all_users[start : start + page_size],
        "meta": {"page": page, "page_size": page_size, "total": len(all_users)},
        "request_id": req_id,
    }


@api_router.get("/departments", summary="List Hierarchical Departments", tags=["Organization"])
async def list_departments(req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    return {
        "data": db.departments,
        "meta": {"page": 1, "page_size": 20, "total": len(db.departments)},
        "request_id": req_id,
    }


@api_router.get("/roles", summary="List Job Roles & Required Competencies", tags=["Organization"])
async def list_roles(req_id: str = Depends(get_request_id)) -> Dict[str, Any]:
    return {
        "data": db.roles,
        "meta": {"page": 1, "page_size": 20, "total": len(db.roles)},
        "request_id": req_id,
    }


@api_router.get("/competencies/me", summary="Get My Competency Profile", tags=["Competencies"])
async def get_my_competencies(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    items = list(db.competencies.values())
    return {
        "data": {
            "user_id": current_user["id"],
            "overall_competency_score": current_user["overall_competency_score"],
            "competencies": items,
        },
        "meta": {"total": len(items)},
        "request_id": req_id,
    }


@api_router.get("/competencies/me/evidence", summary="Get My Competency Evidence", tags=["Competencies"])
async def get_my_evidence(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    user_ev = [e for e in db.evidence if e["user_id"] == current_user["id"]]
    return {
        "data": user_ev,
        "meta": {"page": 1, "page_size": 20, "total": len(user_ev)},
        "request_id": req_id,
    }


@api_router.get("/competencies/me/history", summary="Get My Competency History", tags=["Competencies"])
async def get_my_competency_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    hist = [h for h in db.competency_history if h["user_id"] == current_user["id"]]
    return {
        "data": hist,
        "meta": {"page": 1, "page_size": 20, "total": len(hist)},
        "request_id": req_id,
    }


@api_router.get("/skill-gaps/me", summary="Get My Calculated Skill Gaps", tags=["Skill Gaps"])
async def get_my_skill_gaps(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    gaps = SkillGapService.calculate_gaps_for_user(current_user["id"])
    return {
        "data": gaps,
        "meta": {"page": 1, "page_size": 20, "total": len(gaps)},
        "request_id": req_id,
    }


@api_router.get("/courses", summary="Search & Filter Course Catalogue", tags=["Courses"])
async def list_courses(
    competency: str | None = None,
    provider: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    results = db.courses
    if competency:
        results = [
            c
            for c in results
            if competency.lower() in c["competency"].lower()
            or competency.lower() in c["competency_name"].lower()
        ]
    if provider:
        results = [c for c in results if provider.lower() in c["provider"].lower()]

    start = (page - 1) * page_size
    return {
        "data": results[start : start + page_size],
        "meta": {"page": page, "page_size": page_size, "total": len(results)},
        "request_id": req_id,
    }


@api_router.get("/learning-path/me", summary="Get Personalized Learning Path", tags=["Learning"])
async def get_my_learning_path(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    steps = await RecommendationService.get_or_generate_for_user(current_user["id"])
    return {
        "data": steps,
        "meta": {"page": 1, "page_size": 20, "total": len(steps)},
        "request_id": req_id,
    }


@api_router.get("/recommendations/me", summary="Get Explainable Recommendations", tags=["Recommendations"])
async def get_my_recommendations(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    recs = await RecommendationService.get_or_generate_for_user(current_user["id"])
    return {
        "data": recs,
        "meta": {"page": 1, "page_size": 20, "total": len(recs)},
        "request_id": req_id,
    }


@api_router.post("/assessments/generate", summary="Generate Quiz From Learning Material (Trainer/Admin)", tags=["Assessments"])
async def generate_assessment_from_text(
    payload: QuizGenerateRequest,
    current_user: Dict[str, Any] = Depends(require_roles([Role.TRAINER, Role.ADMIN])),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    now = time.time()
    _quiz_calls[:] = [t for t in _quiz_calls if now - t < 3600]
    if len(_quiz_calls) >= QUIZ_MAX_PER_HOUR:
        raise AppError("RATE_LIMITED", "Quiz generation limit reached for this hour. Please try again later.", status.HTTP_429_TOO_MANY_REQUESTS)
    _quiz_calls.append(now)
    try:
        engine, questions = await generate_quiz(
            payload.text, payload.num_questions, payload.difficulty, payload.competency, payload.title
        )
    except QuizGenerationError as exc:
        raise AppError("UNPROCESSABLE", str(exc), status.HTTP_422_UNPROCESSABLE_ENTITY)
    return {
        "data": {"engine": engine, "questions": questions},
        "meta": {"total_questions": len(questions)},
        "request_id": req_id,
    }


@api_router.get("/assessments", summary="List Assessments", tags=["Assessments"])
async def list_assessments(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    items = [
        {
            "id": a["id"],
            "title": a["title"],
            "competency_id": a["competency_id"],
            "status": a["status"],
            "total_questions": len(a["questions"]),
        }
        for a in db.assessments.values()
    ]
    return {"data": items, "meta": {"total": len(items)}, "request_id": req_id}


@api_router.post("/assessments/{assessment_id}/start", summary="Start Assessment Attempt", tags=["Assessments"])
async def start_assessment(
    assessment_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    if assessment_id not in db.assessments:
        raise AppError("NOT_FOUND", "Assessment not found", status.HTTP_404_NOT_FOUND)
    asmt = db.assessments[assessment_id]
    sanitized_questions = [
        {k: v for k, v in q.items() if k not in ("correct_option", "explanation")}
        for q in asmt["questions"]
    ]
    return {
        "data": {
            "assessment_id": assessment_id,
            "title": asmt["title"],
            "questions": sanitized_questions,
        },
        "meta": {"total_questions": len(sanitized_questions)},
        "request_id": req_id,
    }


@api_router.post("/assessments/{assessment_id}/submit", summary="Submit Assessment & Score on Backend", tags=["Assessments"])
async def submit_assessment(
    assessment_id: str,
    payload: AssessmentSubmitRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    result = AssessmentService.submit_assessment(
        assessment_id=assessment_id,
        user_id=current_user["id"],
        answers=payload.answers,
        request_id=req_id,
    )
    return {"data": result, "meta": {}, "request_id": req_id}


@api_router.get("/assessments/{assessment_id}/results", summary="Get Assessment Results", tags=["Assessments"])
async def get_assessment_results(
    assessment_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    if assessment_id not in db.assessments:
        raise AppError("NOT_FOUND", "Assessment not found", status.HTTP_404_NOT_FOUND)
    asmt = db.assessments[assessment_id]
    if not asmt.get("latest_result"):
        raise AppError("CONFLICT", "Assessment has not been submitted yet", status.HTTP_409_CONFLICT)
    return {"data": asmt["latest_result"], "meta": {}, "request_id": req_id}


@api_router.get(
    "/assessments/{assessment_id}/review",
    summary="Get Full Assessment With Answer Key (Trainer/Admin Only)",
    tags=["Assessments"],
)
async def get_assessment_review(
    assessment_id: str,
    current_user: Dict[str, Any] = Depends(require_roles([Role.TRAINER, Role.ADMIN])),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    if assessment_id not in db.assessments:
        raise AppError("NOT_FOUND", "Assessment not found", status.HTTP_404_NOT_FOUND)
    asmt = db.assessments[assessment_id]
    return {
        "data": {
            "assessment_id": assessment_id,
            "title": asmt["title"],
            "questions": asmt["questions"],
        },
        "meta": {"total_questions": len(asmt["questions"])},
        "request_id": req_id,
    }


@api_router.post("/documents", summary="Upload Learning Document with Validation", tags=["Documents"])
async def upload_document(
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    allowed_exts = {".pdf", ".docx", ".pptx", ".txt"}
    filename = file.filename or "unnamed.pdf"
    if not any(filename.lower().endswith(ext) for ext in allowed_exts):
        raise AppError(
            "UNSUPPORTED_FILE_TYPE",
            "Only PDF, DOCX, PPTX, and TXT files are permitted",
            status.HTTP_400_BAD_REQUEST,
        )
    doc_id = f"doc-{len(db.documents) + 101}"
    record = {
        "id": doc_id,
        "filename": filename,
        "mime_type": file.content_type,
        "status": DocumentStatus.READY_FOR_AI,
        "uploaded_by": current_user["id"],
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    db.documents[doc_id] = record
    db.log_audit(current_user["id"], "DOCUMENT_UPLOAD", doc_id, "SUCCESS", req_id)
    return {"data": record, "meta": {}, "request_id": req_id}


@api_router.get("/analytics/workforce", summary="Workforce Competency Analytics (Admin Only)", tags=["Analytics"])
async def get_workforce_analytics(
    current_user: Dict[str, Any] = Depends(require_roles([Role.ADMIN, Role.SUPER_ADMIN])),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    return {
        "data": {
            "notice": "Demonstration Data",
            "total_officials": 4960,
            "average_competency": 71.0,
            "critical_skill_gaps": 312,
            "training_hours": 18450,
            "assessment_completion_rate": 88.4,
        },
        "meta": {"department_scope": current_user.get("department_id")},
        "request_id": req_id,
    }


@api_router.get("/integrations", summary="Get Ecosystem Integration Status", tags=["Integrations"])
async def list_integrations(
    current_user: Dict[str, Any] = Depends(get_current_user),
    req_id: str = Depends(get_request_id),
) -> Dict[str, Any]:
    igot_state = await igot_adapter.sync()
    nssta_state = await nssta_adapter.sync()
    tpac_state = await tpac_adapter.sync()
    return {
        "data": [igot_state, nssta_state, tpac_state],
        "meta": {"mode": "MOCK"},
        "request_id": req_id,
    }
