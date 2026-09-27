# Frontend-to-Backend API Contract (/api/v1)

All responses follow the standardized envelope:
```json
{
  "data": {},
  "meta": {},
  "request_id": "req-..."
}
```

## Core Endpoints
- `GET /api/v1/health` — System & Adapter readiness
- `POST /api/v1/auth/login` — Authenticate official (Demo: `ananya.sharma@mospi.gov.in` / `StatSaksham@2026`)
- `GET /api/v1/users/me` — Official profile & overall competency score
- `GET /api/v1/competencies/me` — Role competencies, levels, and confidence
- `GET /api/v1/skill-gaps/me` — Server-side calculated role skill gaps
- `GET /api/v1/recommendations/me` — Explainable iGOT & NSSTA recommendations
- `POST /api/v1/assessments/{id}/submit` — Server-side grading & `CompetencyUpdateService` trigger
- `GET /api/v1/assessments` — List assessments (id/title/status/question count)
- `GET /api/v1/assessments/{id}/review` — Full assessment incl. answer key (Trainer/Admin only) — powers the AI Assessment Studio review UI
- `GET /api/v1/analytics/workforce` — Organization-wide competency analytics (Admin only)
- `GET /api/v1/integrations` — iGOT/NSSTA/TPAC adapter sync status (mock mode)
