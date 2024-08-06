from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from src.app.configuration.database import get_session
from src.app.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="client_simple")
def client_simple_fixture(session: Session):
    client = TestClient(app)
    return client
