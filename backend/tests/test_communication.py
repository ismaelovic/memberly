from fastapi.testclient import TestClient
from main import app
from db.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_send_communication():
    response = client.post(
        "/communications",
        json={"type": "email", "content": "Test email content", "member_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["type"] == "email"
    assert response.json()["content"] == "Test email content"


def test_list_communications():
    response = client.get("/communications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
