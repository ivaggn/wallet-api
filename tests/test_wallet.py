import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestSessionlocal = sessionmaker(autocommit=False, autoflush=False,bind=test_engine)

def override_get_db():
    db = TestSessionlocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_create_account():
    response = client.post("/accounts", json={"owner_name": "Ivan"})
    assert response.status_code == 201
    data = response.json()
    assert data["owner_name"] == "Ivan"
    assert data["balance_cents"] == 0

def test_get_account_not_found():
    response = client.get("/accounts/999")
    assert response.status_code == 404

def test_deposit_increases_balance():
    create_response = client.post("/accounts", json={"owner_name": "Ivan"})
    account_id = create_response.json()["id"]

    deposit_response = client.post(f"/accounts/{account_id}/deposit", json={"amount_cents": 500})
    assert deposit_response.status_code == 200
    data = deposit_response.json()
    assert data["balance_cents"] == 500

def test_withdraw_insufficient_funds():
    create_response = client.post("/accounts", json={"owner_name": "Ivan"})
    account_id = create_response.json()["id"]

    withdraw_response = client.post(f"/accounts/{account_id}/withdraw",json={"amount_cents": 500})
    assert withdraw_response.status_code == 400

def test_negative_amount_rejected():
    create_response = client.post("/accounts", json={"owner_name": "Ivan"})
    account_id = create_response.json()["id"]

    deposit_response = client.post(f"/accounts/{account_id}/deposit", json={"amount_cents": -100})
    assert deposit_response.status_code == 422


def test_transfer_success():
    create_response1 = client.post("/accounts", json={"owner_name": "Ivan"})
    account_id1 = create_response1.json()["id"]

    create_response2 = client.post("/accounts" , json={"owner_name": "Joe"})
    account_id2 = create_response2.json()["id"]

    deposit_response = client.post(f"/accounts/{account_id1}/deposit", json={"amount_cents" : 1000})

    transfer_response = client.post("/transfers", json={
        "from_id": account_id1,
        "to_id": account_id2,
        "amount_cents": 300
    })

    assert transfer_response.status_code == 200
    data = transfer_response.json()
    assert data["sender"]["balance_cents"] == 700
    assert data["receiver"]["balance_cents"] == 300

def test_transfer_insufficient_funds_leaves_balances_unchanged():
    create_response1 = client.post("/accounts", json={"owner_name": "Ivan"})
    account_id1 = create_response1.json()["id"]

    create_response2 = client.post("/accounts", json={"owner_name": "Joe"})
    account_id2 = create_response2.json()["id"]

    transfer_response = client.post("/transfers", json={
        "from_id": account_id1,
        "to_id": account_id2,
        "amount_cents": 500
    })
    assert transfer_response.status_code == 400

    check_response = client.get(f"/accounts/{account_id1}")
    
    assert check_response.json()["balance_cents"] == 0

client = TestClient(app)