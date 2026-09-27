# Security Baseline

1. **Password Hashing**: PBKDF2-HMAC-SHA256 / Bcrypt password hashing; zero plaintext storage.
2. **RBAC Enforcement**: Determined strictly from backend JWT identity (`LEARNER`, `TRAINER`, `ADMIN`, `INTEGRATION_ADMIN`, `SUPER_ADMIN`).
3. **Request Traceability**: Every request preserves or generates `X-Request-ID` across headers, responses, and audit logs.
4. **Server-Side Scoring**: Frontend never submits scores or skill-gap deltas; backend validates and computes all outcomes.
