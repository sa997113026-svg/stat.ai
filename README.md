# StatSaksham AI — Full-Stack Prototype (SIH 2026, PS ID26101)

This package contains both halves of the prototype, wired together:

```
statsaksham-backend/     FastAPI modular monolith (in-memory demo DB, JWT auth, seeded data)
StatSaksham-AI/          Next.js frontend (App Router)
```

The frontend now has a real service layer (`lib/apiClient.ts` + `lib/services.ts`)
that calls the backend's `/api/v1` endpoints, auto-logging in with the seeded
demo accounts and mapping backend response shapes onto the frontend's types.
If the backend isn't running (or a call fails), every page **falls back to the
bundled mock data automatically** — the UI never breaks, it just quietly
degrades from "Live Backend" to "Demo Data".

## What is actually wired end-to-end

| Page | Backend calls |
|---|---|
| Dashboard | `GET /users/me`, `/competencies/me`, `/skill-gaps/me`, `/courses` |
| My Competency Profile | `GET /competencies/me`, `/users/me` |
| Skill Gaps | `GET /skill-gaps/me` |
| Learning Path | `GET /courses` |
| Diagnostic Assessment | `POST /assessments/{id}/start` → answer → `POST /assessments/{id}/submit` (real server-side grading + competency level update, not simulated) |
| AI Assessment Studio | `GET /assessments/{id}/review` (trainer-role token) — the seeded, source-cited question bank |
| iGOT Integration | `GET /integrations` |
| Admin Workforce Dashboard | `GET /analytics/workforce` (admin-role token) |

Two small endpoints were added to the backend to support this
(`GET /assessments`, `GET /assessments/{id}/review`) — see
`statsaksham-backend/docs/API_CONTRACT.md`. Everything else in the backend is
unchanged from the original zip.

## Run it

**1. Backend** (terminal 1):
```bash
cd statsaksham-backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Swagger docs: http://localhost:8000/docs

**2. Frontend** (terminal 2):
```bash
cd StatSaksham-AI
npm install
npm run dev
```
Open http://localhost:3000

The frontend ships with `.env.local` already set to:
```
NEXT_PUBLIC_API_MODE=live
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```
Set `NEXT_PUBLIC_API_MODE=mock` (or just don't start the backend) to run the
frontend as a standalone static demo instead.

## Demo accounts (seeded by the backend, documented in its API contract)

| Role | Email | Password |
|---|---|---|
| Learner (Ananya Sharma, SSO) | ananya.sharma@mospi.gov.in | StatSaksham@2026 |
| Trainer (Dr. Rajeshwar Verma) | trainer@nssta.gov.in | Trainer@2026 |
| Admin (Vikramaditya Sen) | admin@mospi.gov.in | Admin@2026 |

The frontend logs in with these automatically per-page (no login screen yet) —
you don't need to enter them anywhere, they're just documented here for
reference and for exploring `/docs` directly.

## Known limitations (honest, prototype-stage)

- The backend's "database" is in-memory and resets on restart — fine for a
  demo, not for production.
- `ai/interfaces.py`'s document→question generator is a stub (`generate_questions_from_document`
  returns `[]`); the Assessment Studio instead surfaces the seeded,
  already-reviewed question bank via the new `/review` endpoint, so the
  "generate" button demonstrates the real trainer-review data path rather than
  live document parsing.
- The admin dashboard's heatmap/emerging-skills panels are still static
  demo numbers; only the top KPI strip is live-wired (the backend doesn't
  expose per-skill breakdowns yet).
- `training_videos.json` (uploaded alongside this) was empty, so it isn't
  referenced anywhere yet — send its contents if you want it incorporated.
- No automated frontend build/type-check was run in this environment (no
  network access to `npm install`); the backend's own `pytest` suite is
  unaffected by the two additive endpoints. Run `npm run build` yourself on
  first setup to confirm.
