from fastapi.testclient import TestClient
from app.main import app
from app.repositories.in_memory import db

client = TestClient(app)


def test_health_and_request_id_header():
    response = client.get("/api/v1/health", headers={"X-Request-ID": "test-req-001"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-req-001"
    body = response.json()
    assert body["data"]["status"] == "healthy"
    assert body["request_id"] == "test-req-001"


def test_complete_golden_thread_e2e_flow():
    """
    Verifies the complete SIH 26101 E2E Journey:
    LOGIN -> GET PROFILE -> GET COMPETENCIES -> GET SKILL GAPS ->
    GET RECOMMENDATIONS -> GET LEARNING PATH -> START ASSESSMENT ->
    SUBMIT ASSESSMENT -> GET RESULT & VERIFY COMPETENCY UPGRADE
    """
    db.reset_and_seed()

    # 1. LOGIN
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "ananya.sharma@mospi.gov.in", "password": "StatSaksham@2026"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. GET PROFILE
    me_res = client.get("/api/v1/users/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["data"]["name"] == "Ananya Sharma"
    assert me_res.json()["data"]["overall_competency_score"] == 67

    # 3. GET COMPETENCIES
    comp_res = client.get("/api/v1/competencies/me", headers=headers)
    assert comp_res.status_code == 200
    assert len(comp_res.json()["data"]["competencies"]) == 6

    # 4. GET SKILL GAPS
    gaps_res = client.get("/api/v1/skill-gaps/me", headers=headers)
    assert gaps_res.status_code == 200
    gaps = gaps_res.json()["data"]
    assert any(g["competency_id"] == "comp-python" and g["gap"] == 2 for g in gaps)

    # 5. GET RECOMMENDATIONS & LEARNING PATH
    rec_res = client.get("/api/v1/recommendations/me", headers=headers)
    assert rec_res.status_code == 200
    assert len(rec_res.json()["data"]) >= 2

    path_res = client.get("/api/v1/learning-path/me", headers=headers)
    assert path_res.status_code == 200

    # 6. START ASSESSMENT
    start_res = client.post("/api/v1/assessments/asmt-plfs-2026/start", headers=headers)
    assert start_res.status_code == 200
    questions = start_res.json()["data"]["questions"]
    assert "correct_option" not in questions[0]

    # 7. SUBMIT ASSESSMENT (100% score upgrades Python Level 2 -> Level 3)
    submit_res = client.post(
        "/api/v1/assessments/asmt-plfs-2026/submit",
        headers=headers,
        json={"answers": {"q-plfs-01": "B", "q-plfs-02": "A"}},
    )
    assert submit_res.status_code == 200
    result_data = submit_res.json()["data"]
    assert result_data["score_percent"] == 100.0
    assert result_data["competency_update"]["previous_level"] == 2
    assert result_data["competency_update"]["new_level"] == 3

    # 8. GET RESULT & VERIFY UPDATED PROFILE SCORE
    res_check = client.get("/api/v1/assessments/asmt-plfs-2026/results", headers=headers)
    assert res_check.status_code == 200

    updated_me = client.get("/api/v1/users/me", headers=headers)
    assert updated_me.json()["data"]["overall_competency_score"] == 76


def test_rbac_blocks_learner_from_admin_workforce_endpoint():
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "ananya.sharma@mospi.gov.in", "password": "StatSaksham@2026"},
    )
    token = login_res.json()["data"]["access_token"]
    admin_res = client.get(
        "/api/v1/analytics/workforce",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert admin_res.status_code == 403
