from datetime import datetime, timezone
from typing import Any, Dict, List
from app.core.security import hash_password
from app.domain.enums import (
    AssessmentStatus,
    CompetencyDomain,
    DocumentStatus,
    EvidenceType,
    LearningStatus,
    QuestionStatus,
    QuestionType,
    Role,
    UserStatus,
)


class InMemoryDatabase:
    def __init__(self) -> None:
        self.reset_and_seed()

    def reset_and_seed(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = {
            "usr-sso-4092": {
                "id": "usr-sso-4092",
                "name": "Ananya Sharma",
                "email": "ananya.sharma@mospi.gov.in",
                "password_hash": hash_password("StatSaksham@2026"),
                "designation": "Senior Statistical Officer (SSO)",
                "department": "Labour Bureau & Periodic Labour Force Survey (PLFS) Division",
                "department_id": "dept-plfs",
                "job_role": "role-sso-plfs",
                "current_assignment": "Automated Microdata Validation & High-Frequency Labour Indicators",
                "experience_years": 7,
                "education": ["M.Sc. Statistics, University of Delhi"],
                "languages": ["English", "Hindi"],
                "role": Role.LEARNER,
                "status": UserStatus.ACTIVE,
                "overall_competency_score": 67,
            },
            "usr-trainer-101": {
                "id": "usr-trainer-101",
                "name": "Dr. Rajeshwar Verma",
                "email": "trainer@nssta.gov.in",
                "password_hash": hash_password("Trainer@2026"),
                "designation": "Joint Director & Faculty (Sampling)",
                "department": "National Statistical Systems Training Academy (NSSTA)",
                "department_id": "dept-nssta",
                "job_role": "role-trainer",
                "current_assignment": "Survey Methodology & AI Question Bank Curation",
                "experience_years": 16,
                "education": ["Ph.D. Survey Sampling"],
                "languages": ["English", "Hindi"],
                "role": Role.TRAINER,
                "status": UserStatus.ACTIVE,
                "overall_competency_score": 92,
            },
            "usr-admin-001": {
                "id": "usr-admin-001",
                "name": "Vikramaditya Sen",
                "email": "admin@mospi.gov.in",
                "password_hash": hash_password("Admin@2026"),
                "designation": "Deputy Director General (Capacity Building)",
                "department": "MoSPI Central Training & Workforce Cell",
                "department_id": "dept-mospi-hq",
                "job_role": "role-ddg",
                "current_assignment": "National Statistical Workforce Readiness",
                "experience_years": 22,
                "education": ["Indian Statistical Service (ISS)"],
                "languages": ["English", "Hindi"],
                "role": Role.ADMIN,
                "status": UserStatus.ACTIVE,
                "overall_competency_score": 95,
            },
        }

        self.departments: List[Dict[str, Any]] = [
            {
                "id": "dept-plfs",
                "name": "Periodic Labour Force Survey (PLFS) Division",
                "ministry": "Ministry of Statistics & Programme Implementation (Demonstration)",
                "division": "National Sample Survey Office (NSSO)",
                "unit": "Urban & Rural Frame Analytics Unit",
            },
            {
                "id": "dept-nssta",
                "name": "National Statistical Systems Training Academy (NSSTA)",
                "ministry": "Ministry of Statistics & Programme Implementation (Demonstration)",
                "division": "Capacity Building Division",
                "unit": "Greater Noida Campus",
            },
        ]

        self.roles: List[Dict[str, Any]] = [
            {
                "id": "role-sso-plfs",
                "name": "Senior Statistical Officer (SSO) — Labour Statistics",
                "description": "Responsible for unit-level microdata validation, multiplier estimation, and quarterly bulletin preparation.",
                "department": "dept-plfs",
                "activities": [
                    "Validate PLFS household and person-level survey schedules",
                    "Compute Relative Standard Error (RSE) and rotational panel multipliers",
                    "Automate reproducible tabulation scripts using Python Pandas",
                ],
                "required_competencies": [
                    {"competency_id": "comp-python", "required_level": 4},
                    {"competency_id": "comp-sampling", "required_level": 4},
                    {"competency_id": "comp-viz", "required_level": 4},
                    {"competency_id": "comp-api", "required_level": 3},
                    {"competency_id": "comp-labour", "required_level": 4},
                    {"competency_id": "comp-quality", "required_level": 3},
                ],
            }
        ]

        self.competencies: Dict[str, Dict[str, Any]] = {
            "comp-python": {
                "id": "comp-python",
                "name": "Python for Statistical Computing",
                "domain": CompetencyDomain.TECHNICAL,
                "description": "Vectorized microdata processing, survey weight application, and automated validation pipelines.",
                "subskills": ["Pandas Vectorization", "Multiplier Weighting", "Automated Editing"],
                "current_level": 2,
                "required_level": 4,
                "confidence": 0.87,
                "trend": "up",
                "why_it_matters": "Mandatory for migrating quarterly PLFS unit-level tabulation pipelines from legacy desktop scripts to reproducible Python workflows.",
            },
            "comp-sampling": {
                "id": "comp-sampling",
                "name": "Multi-Stage Stratified Sampling Methods",
                "domain": CompetencyDomain.STATISTICAL,
                "description": "Design of PPS selection, rotational panel estimation, and Relative Standard Error (RSE) calculation.",
                "subskills": ["PPS Selection", "Rotational Panels", "Variance & RSE"],
                "current_level": 2,
                "required_level": 4,
                "confidence": 0.91,
                "trend": "stable",
                "why_it_matters": "Required for designing rotational panel weights and RSE estimations in urban frame survey blocks.",
            },
            "comp-viz": {
                "id": "comp-viz",
                "name": "Interactive Data Visualization & Dissemination",
                "domain": CompetencyDomain.TECHNICAL,
                "description": "Designing accessible statistical charts and public indicator dashboards.",
                "subskills": ["Confidence Fan Charts", "WCAG Data Tables", "e-Sankhyiki Dashboards"],
                "current_level": 3,
                "required_level": 4,
                "confidence": 0.84,
                "trend": "up",
                "why_it_matters": "Needed to publish accessible public-facing dashboards aligned with e-Sankhyiki standards.",
            },
            "comp-api": {
                "id": "comp-api",
                "name": "API Architecture & Open Government Data (SDMX)",
                "domain": CompetencyDomain.DIGITAL_GOVERNANCE,
                "description": "RESTful JSON and SDMX 3.0 statistical metadata exchange standards.",
                "subskills": ["SDMX 3.0 Schemas", "Open Data APIs"],
                "current_level": 2,
                "required_level": 3,
                "confidence": 0.82,
                "trend": "stable",
                "why_it_matters": "Enables automated machine-to-machine dissemination of macro-indicators.",
            },
            "comp-labour": {
                "id": "comp-labour",
                "name": "Labour Force & Employment Frameworks (ICLS)",
                "domain": CompetencyDomain.STATISTICAL,
                "description": "Usual Status (ps+ss) and Current Weekly Status (CWS) classification standards.",
                "subskills": ["CWS 7-Day Reference", "Usual Principal Status"],
                "current_level": 4,
                "required_level": 4,
                "confidence": 0.95,
                "trend": "up",
                "why_it_matters": "Core domain mandate for labour force indicator compilation.",
            },
            "comp-quality": {
                "id": "comp-quality",
                "name": "Official Data Quality Assurance & Anonymization",
                "domain": CompetencyDomain.BEHAVIOURAL_MANAGERIAL,
                "description": "Statistical disclosure control and unit-level microdata anonymization.",
                "subskills": ["Disclosure Control", "DPDP Compliance"],
                "current_level": 3,
                "required_level": 3,
                "confidence": 0.89,
                "trend": "stable",
                "why_it_matters": "Ensures microdata releases adhere to privacy norms.",
            },
        }

        self.evidence: List[Dict[str, Any]] = [
            {
                "id": "ev-101",
                "user_id": "usr-sso-4092",
                "competency_id": "comp-python",
                "source": "StatSaksham AI Diagnostic Engine",
                "title": "Diagnostic Assessment: Python DataFrames & Vectorization",
                "type": EvidenceType.ASSESSMENT,
                "date": "2026-09-12",
                "score": 54.0,
                "confidence": 0.87,
                "metadata": {"outcome": "Level 2 Verified"},
            },
            {
                "id": "ev-102",
                "user_id": "usr-sso-4092",
                "competency_id": "comp-python",
                "source": "iGOT Karmayogi Telemetry",
                "title": "iGOT Course: Foundations of Programming for Data Officers",
                "type": EvidenceType.COURSE_COMPLETION,
                "date": "2026-07-19",
                "score": 81.0,
                "confidence": 0.90,
                "metadata": {"outcome": "Completed"},
            },
        ]

        self.competency_history: List[Dict[str, Any]] = [
            {
                "id": "hist-001",
                "user_id": "usr-sso-4092",
                "competency_id": "comp-python",
                "previous_level": 1,
                "new_level": 2,
                "evidence_id": "ev-102",
                "confidence": 0.87,
                "calculated_at": "2026-07-19T14:20:00Z",
            }
        ]

        self.courses: List[Dict[str, Any]] = [
            {
                "id": "crs-igot-python-01",
                "title": "Python for Official Statistical Analysis & Microdata Processing",
                "provider": "iGOT Karmayogi",
                "domain": CompetencyDomain.TECHNICAL,
                "competency": "comp-python",
                "competency_name": "Python for Statistical Computing",
                "difficulty": "Intermediate",
                "duration": "4 hours 30 mins",
                "language": "English / Hindi",
                "format": "Self-Paced Online",
                "match_score": 0.94,
            },
            {
                "id": "crs-nssta-sampling-02",
                "title": "Advanced Multi-Stage Sampling & Variance Estimation in Household Surveys",
                "provider": "NSSTA",
                "domain": CompetencyDomain.STATISTICAL,
                "competency": "comp-sampling",
                "competency_name": "Multi-Stage Stratified Sampling Methods",
                "difficulty": "Advanced",
                "duration": "5 Days (30 Hours)",
                "language": "English",
                "format": "Hybrid Cohort",
                "match_score": 0.96,
            },
            {
                "id": "crs-igot-viz-03",
                "title": "Advanced Data Visualization for Public Statistical Portals",
                "provider": "iGOT Karmayogi",
                "domain": CompetencyDomain.TECHNICAL,
                "competency": "comp-viz",
                "competency_name": "Interactive Data Visualization & Dissemination",
                "difficulty": "Intermediate",
                "duration": "3 hours",
                "language": "English / Hindi",
                "format": "Self-Paced Online",
                "match_score": 0.89,
            },
        ]

        self.learning_progress: Dict[str, Dict[str, Any]] = {
            "crs-igot-python-01": {
                "user_id": "usr-sso-4092",
                "course_id": "crs-igot-python-01",
                "status": LearningStatus.IN_PROGRESS,
                "progress_percentage": 45,
                "learning_hours": 2.1,
                "started_at": "2026-09-15T09:00:00Z",
                "completed_at": None,
                "score": None,
            }
        }

        self.assessments: Dict[str, Dict[str, Any]] = {
            "asmt-plfs-2026": {
                "id": "asmt-plfs-2026",
                "title": "PLFS Sampling Design & Python Multiplier Verification",
                "competency_id": "comp-python",
                "status": AssessmentStatus.PUBLISHED,
                "assigned_user_id": "usr-sso-4092",
                "questions": [
                    {
                        "id": "q-plfs-01",
                        "assessment_id": "asmt-plfs-2026",
                        "text": "In the Periodic Labour Force Survey (PLFS) urban rotational panel scheme, what proportion of First Stage Units (FSUs) is replaced in each subsequent quarter?",
                        "type": QuestionType.MCQ,
                        "options": [
                            {"key": "A", "text": "10% of the selected urban FSUs"},
                            {"key": "B", "text": "25% of the selected urban FSUs (4-quarter rotation)"},
                            {"key": "C", "text": "50% of the selected urban FSUs"},
                            {"key": "D", "text": "100% retained without replacement"},
                        ],
                        "correct_option": "B",
                        "explanation": "25% of urban FSUs are rotated every quarter to maintain 75% longitudinal overlap.",
                        "difficulty": "Medium",
                        "competency": "comp-sampling",
                        "source": {
                            "document_title": "PLFS_Methodology_and_Sampling_Design_Manual_v4.pdf",
                            "page_number": 12,
                            "section": "Section 2.4",
                        },
                        "confidence": 0.96,
                        "status": QuestionStatus.APPROVED,
                    },
                    {
                        "id": "q-plfs-02",
                        "assessment_id": "asmt-plfs-2026",
                        "text": "While applying survey design weights (multipliers) to household-level microdata in Python, which formula computes the pooled combined subsample estimate (NSC=2)?",
                        "type": QuestionType.MCQ,
                        "options": [
                            {"key": "A", "text": "Final Weight = MLT / 200 when SS1 and SS2 are combined"},
                            {"key": "B", "text": "Final Weight = MLT * 100"},
                            {"key": "C", "text": "Final Weight = Simple unweighted mean"},
                            {"key": "D", "text": "Final Weight = MLT / 1000"},
                        ],
                        "correct_option": "A",
                        "explanation": "Posted MLT is divided by 100 for single subsample or 200 when pooling both independent subsamples.",
                        "difficulty": "Medium",
                        "competency": "comp-python",
                        "source": {
                            "document_title": "PLFS_Methodology_and_Sampling_Design_Manual_v4.pdf",
                            "page_number": 44,
                            "section": "Annexure III",
                        },
                        "confidence": 0.95,
                        "status": QuestionStatus.APPROVED,
                    },
                ],
                "latest_result": None,
            }
        }

        self.documents: Dict[str, Dict[str, Any]] = {
            "doc-plfs-manual-2026": {
                "id": "doc-plfs-manual-2026",
                "filename": "PLFS_Methodology_and_Sampling_Design_Manual_v4.pdf",
                "mime_type": "application/pdf",
                "size_bytes": 4404019,
                "pages": 68,
                "status": DocumentStatus.READY_FOR_AI,
                "uploaded_by": "usr-sso-4092",
                "uploaded_at": "2026-09-20T10:15:00Z",
            }
        }

        self.notifications: List[Dict[str, Any]] = [
            {
                "id": "notif-01",
                "user_id": "usr-sso-4092",
                "type": "ASSESSMENT_REMINDER",
                "message": "Your Python competency verification assessment is due.",
                "is_read": False,
                "created_at": "2026-09-27T08:00:00Z",
            },
            {
                "id": "notif-02",
                "user_id": "usr-sso-4092",
                "type": "RECOMMENDATION_MATCH",
                "message": "A new NSSTA programme on Multi-Stage Sampling matches your learning path.",
                "is_read": False,
                "created_at": "2026-09-27T09:30:00Z",
            },
        ]

        self.audit_logs: List[Dict[str, Any]] = []

    def log_audit(
        self,
        user_id: str,
        action: str,
        resource: str,
        result: str,
        request_id: str,
        metadata: Dict[str, Any] | None = None,
    ) -> None:
        self.audit_logs.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "user": user_id,
                "action": action,
                "resource": resource,
                "result": result,
                "request_id": request_id,
                "metadata": metadata or {},
            }
        )


db = InMemoryDatabase()
