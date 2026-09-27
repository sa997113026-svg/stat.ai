# StatSaksham AI — Part 2: FastAPI Modular Monolith Backend

**AI-Powered Skill Intelligence & Capacity Building for India's Official Statistical System (SIH 2026 — Problem ID 26101)**

## Quick Start in VS Code

1. Extract `statsaksham-backend.zip` and open the folder in **VS Code**.
2. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. Open Swagger OpenAPI documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)
5. Run the automated E2E Pytest suite:
   ```bash
   pytest -v
   ```
