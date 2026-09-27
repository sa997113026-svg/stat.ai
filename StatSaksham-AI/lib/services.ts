import { competencies, courses, demoUser, gaps, questions } from '../data/mock';
import { Competency, Course, CompetencyDomain as FEDomain, Question, SkillGap } from '../types';
import { apiGet, apiPost, isLiveMode } from './apiClient';

// ---------------------------------------------------------------------------
// Backend <-> frontend shape adapters
// ---------------------------------------------------------------------------

const DOMAIN_MAP: Record<string, FEDomain> = {
  STATISTICAL: 'Statistical',
  TECHNICAL: 'Technical',
  DIGITAL_GOVERNANCE: 'Digital Governance',
  BEHAVIOURAL_MANAGERIAL: 'Behavioural & Managerial',
};

const COMPETENCY_NAMES: Record<string, string> = {
  'comp-python': 'Python for Statistical Computing',
  'comp-sampling': 'Multi-Stage Stratified Sampling Methods',
  'comp-viz': 'Interactive Data Visualization & Dissemination',
  'comp-api': 'API Architecture & Open Government Data (SDMX)',
  'comp-labour': 'Labour Force & Employment Frameworks (ICLS)',
  'comp-quality': 'Official Data Quality Assurance & Anonymization',
};

const TREND_MAP: Record<string, number> = { up: 6, stable: 2, down: -3 };

type BECompetency = {
  id: string; name: string; domain: string; current_level: number; required_level: number;
  confidence: number; trend: string;
};
type BEGap = {
  competency_id: string; competency_name: string; domain: string; current_level: number;
  required_level: number; priority: 'high' | 'medium' | 'low'; confidence: number; why_it_matters: string;
};
type BECourse = {
  id: string; title: string; provider: string; domain: string; competency_name: string;
  difficulty: string; duration: string; language: string; match_score: number;
};
type BEQuestionOption = { key: string; text: string };
type BEReviewQuestion = {
  id: string; text: string; options: BEQuestionOption[]; correct_option: string; explanation: string;
  difficulty: string; competency: string; confidence: number;
  source: { document_title: string; page_number: number; section: string };
};

function mapCompetency(c: BECompetency): Competency {
  return {
    id: c.id,
    name: c.name,
    domain: (DOMAIN_MAP[c.domain] ?? 'Technical') as FEDomain,
    current: Math.round(c.current_level * 20),
    required: Math.round(c.required_level * 20),
    confidence: Math.round(c.confidence * 100),
    trend: TREND_MAP[c.trend] ?? 0,
    evidenceCount: 0,
  };
}

function mapGap(g: BEGap): SkillGap {
  return {
    competencyId: g.competency_id,
    competencyName: g.competency_name,
    domain: (DOMAIN_MAP[g.domain] ?? 'Technical') as FEDomain,
    currentLevel: g.current_level,
    requiredLevel: g.required_level,
    priority: g.priority,
    confidence: Math.round(g.confidence * 100),
    reason: g.why_it_matters,
    nextAction: `Complete the recommended learning path for ${g.competency_name}.`,
  };
}

function mapCourse(c: BECourse): Course {
  return {
    id: c.id,
    title: c.title,
    provider: c.provider,
    competency: c.competency_name,
    domain: (DOMAIN_MAP[c.domain] ?? 'Technical') as FEDomain,
    difficulty: (c.difficulty as Course['difficulty']) ?? 'Intermediate',
    duration: c.duration,
    language: c.language,
    match: Math.round(c.match_score * 100),
    status: 'Recommended',
  };
}

function mapReviewQuestion(q: BEReviewQuestion): Question {
  const answerIndex = q.options.findIndex((o) => o.key === q.correct_option);
  return {
    id: q.id,
    question: q.text,
    options: q.options.map((o) => o.text),
    answer: answerIndex >= 0 ? answerIndex : 0,
    explanation: q.explanation,
    competency: COMPETENCY_NAMES[q.competency] ?? q.competency,
    difficulty: (q.difficulty as Question['difficulty']) ?? 'Medium',
    source: `${q.source.document_title} · Page ${q.source.page_number} · ${q.source.section}`,
    confidence: Math.round(q.confidence * 100),
  };
}

async function withMockFallback<T>(fn: () => Promise<T>, fallback: T): Promise<T> {
  if (!isLiveMode()) return new Promise((r) => setTimeout(() => r(fallback), 120));
  try {
    return await fn();
  } catch {
    // Backend not reachable (not started, wrong URL, etc.) — degrade to demo data
    // rather than breaking the prototype UI.
    return fallback;
  }
}

// ---------------------------------------------------------------------------
// Public service functions (used by pages)
// ---------------------------------------------------------------------------

export async function getCompetencyProfile(): Promise<Competency[]> {
  return withMockFallback(async () => {
    const data = await apiGet<{ competencies: BECompetency[] }>('/competencies/me', 'learner');
    return data.competencies.map(mapCompetency);
  }, competencies);
}

export async function getSkillGaps(): Promise<SkillGap[]> {
  return withMockFallback(async () => {
    const data = await apiGet<BEGap[]>('/skill-gaps/me', 'learner');
    return data.map(mapGap);
  }, gaps);
}

export async function getCourses(): Promise<Course[]> {
  return withMockFallback(async () => {
    const data = await apiGet<BECourse[]>('/courses', 'learner');
    return data.map(mapCourse);
  }, courses);
}

export async function getQuestions(): Promise<Question[]> {
  return withMockFallback(async () => {
    const data = await apiGet<{ questions: BEReviewQuestion[] }>(
      '/assessments/asmt-plfs-2026/review',
      'trainer'
    );
    return data.questions.map(mapReviewQuestion);
  }, questions);
}

export type ProfileSummary = {
  name: string;
  designation: string;
  department: string;
  experience: string;
  assignment: string;
  lastAssessment: string;
  learningHours: number;
  overallScore: number;
};

export async function getMyProfile(): Promise<ProfileSummary> {
  const fallback: ProfileSummary = {
    name: demoUser.name,
    designation: demoUser.designation,
    department: demoUser.department,
    experience: demoUser.experience,
    assignment: demoUser.assignment,
    lastAssessment: demoUser.lastAssessment,
    learningHours: demoUser.learningHours,
    overallScore: 67,
  };
  return withMockFallback(async () => {
    const u = await apiGet<{
      name: string; designation: string; department: string; experience_years: number;
      current_assignment: string; overall_competency_score: number;
    }>('/users/me', 'learner');
    return {
      name: u.name,
      designation: u.designation,
      department: u.department,
      experience: `${u.experience_years} years`,
      assignment: u.current_assignment,
      lastAssessment: fallback.lastAssessment,
      learningHours: fallback.learningHours,
      overallScore: u.overall_competency_score,
    };
  }, fallback);
}

export async function syncIGOT(): Promise<{ status: string; synced: number; lastSync: string }> {
  const fallback = { status: 'Connected', synced: 1284, lastSync: new Date().toLocaleTimeString() };
  return withMockFallback(async () => {
    const data = await apiGet<
      { status: string; records_synced: number; last_sync: string }[]
    >('/integrations', 'learner');
    const igot = data[0];
    return {
      status: igot.status,
      synced: igot.records_synced,
      lastSync: new Date(igot.last_sync).toLocaleTimeString(),
    };
  }, fallback);
}

export async function generateAssessment(): Promise<Question[]> {
  // In live mode this pulls the seeded, trainer-reviewed AI question bank
  // (POST-generation, human-in-the-loop demo) rather than fabricating new
  // questions client-side.
  return withMockFallback(async () => {
    const data = await apiGet<{ questions: BEReviewQuestion[] }>(
      '/assessments/asmt-plfs-2026/review',
      'trainer'
    );
    return data.questions.map(mapReviewQuestion);
  }, questions);
}

// ---------------------------------------------------------------------------
// Live assessment-taking flow (backend-graded)
// ---------------------------------------------------------------------------

export type LiveAssessmentQuestion = {
  id: string;
  text: string;
  options: BEQuestionOption[];
  difficulty: string;
  competency: string;
};

export async function startAssessment(
  assessmentId = 'asmt-plfs-2026'
): Promise<{ title: string; questions: LiveAssessmentQuestion[] } | null> {
  if (!isLiveMode()) return null;
  try {
    const data = await apiGet<{ title: string; questions: LiveAssessmentQuestion[] }>(
      `/assessments/${assessmentId}/start`,
      'learner'
    );
    return data;
  } catch {
    return null;
  }
}

export type AssessmentResult = {
  score_percent: number;
  correct_answers: number;
  incorrect_answers: number;
  total_questions: number;
  competency_update: { previous_level: number; new_level: number } | null;
};

export async function submitAssessment(
  assessmentId: string,
  answers: Record<string, string>
): Promise<AssessmentResult | null> {
  if (!isLiveMode()) return null;
  try {
    return await apiPost<AssessmentResult>(`/assessments/${assessmentId}/submit`, { answers }, 'learner');
  } catch {
    return null;
  }
}

export async function getWorkforceAnalytics() {
  const fallback = {
    total_officials: 4821,
    average_competency: 64,
    critical_skill_gaps: 17,
    training_hours: 21438,
    assessment_completion_rate: 82,
  };
  return withMockFallback(async () => {
    return await apiGet<typeof fallback>('/analytics/workforce', 'admin');
  }, fallback);
}
