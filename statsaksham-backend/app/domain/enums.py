from enum import Enum


class Role(str, Enum):
    LEARNER = "LEARNER"
    TRAINER = "TRAINER"
    ADMIN = "ADMIN"
    INTEGRATION_ADMIN = "INTEGRATION_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class CompetencyDomain(str, Enum):
    STATISTICAL = "STATISTICAL"
    TECHNICAL = "TECHNICAL"
    DIGITAL_GOVERNANCE = "DIGITAL_GOVERNANCE"
    BEHAVIOURAL_MANAGERIAL = "BEHAVIOURAL_MANAGERIAL"


class ProficiencyLevel(int, Enum):
    BEGINNER = 1
    BASIC = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class SkillGapPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LearningStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class AssessmentStatus(str, Enum):
    DRAFT = "DRAFT"
    GENERATING = "GENERATING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class QuestionType(str, Enum):
    MCQ = "MCQ"
    TRUE_FALSE = "TRUE_FALSE"
    QUIZ = "QUIZ"
    SCENARIO = "SCENARIO"


class QuestionStatus(str, Enum):
    AI_GENERATED = "AI_GENERATED"
    TRAINER_REVIEW = "TRAINER_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"


class EvidenceType(str, Enum):
    EDUCATION = "EDUCATION"
    TRAINING = "TRAINING"
    ASSESSMENT = "ASSESSMENT"
    COURSE_COMPLETION = "COURSE_COMPLETION"
    PRACTICAL_EXERCISE = "PRACTICAL_EXERCISE"
    SELF_DECLARATION = "SELF_DECLARATION"
    SUPERVISOR_ASSESSMENT = "SUPERVISOR_ASSESSMENT"
    OTHER = "OTHER"


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
    QUARANTINED = "QUARANTINED"
    READY_FOR_AI = "READY_FOR_AI"


class IntegrationStatus(str, Enum):
    CONNECTED = "Connected"
    SYNCHRONIZING = "Synchronizing"
    NEEDS_ATTENTION = "Needs Attention"
    OFFLINE = "Offline"
