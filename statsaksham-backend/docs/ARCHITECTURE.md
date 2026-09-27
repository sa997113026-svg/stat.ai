# StatSaksham AI — Modular Monolith Architecture

## Layered Architecture
`Next.js Frontend -> FastAPI Router (/api/v1) -> Application Services -> Domain Models -> Repository Interfaces -> InMemory / PostgreSQL Persistence`

## Pluggable Adapters
- **Government Ecosystem Adapters**: `IGOTAdapter`, `NSSTAAdapter`, `TPACAdapter`
- **AI Service Interfaces**: `AIRecommendationProvider`, `AIAssessmentProvider`, `AITutorProvider`
