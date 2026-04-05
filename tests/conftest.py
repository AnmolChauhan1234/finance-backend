import pytest
from fastapi.testclient import TestClient
from app.main import app
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
def test_client():
    return TestClient(app)