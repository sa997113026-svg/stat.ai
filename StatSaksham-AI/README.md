# StatSaksham AI

AI Skill Intelligence & Capacity Building for India's Official Statistical System.

SIH 2026 – Problem Statement 26101 frontend prototype.

## What is included

- Government-grade public landing page
- Learner dashboard focused on Role → Competency → Gap → Learning → Assessment → Improvement
- Competency intelligence and evidence UI
- Skill-gap analysis
- Personalized learning path
- iGOT integration-ready service layer with mock mode
- AI Assessment Studio mock flow
- Assessment player with competency results
- Workforce intelligence admin dashboard
- Accessibility-minded design system
- Responsive layouts
- Fictional demo data only

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Build

```bash
npm run build
npm start
```

## API mode

Set `NEXT_PUBLIC_API_MODE=mock` for the included demo adapter. Replace the service implementations in `lib/services.ts` with authenticated backend calls when an authorized integration is available.

## Design references

The `public/references/` directory contains the screenshots supplied for this design exercise. They are included only as visual references.

## Important

This is a prototype. It does not claim official government endorsement or live iGOT/NSSTA integration. All demo people, metrics and course records are fictional unless explicitly replaced with authorized data.
