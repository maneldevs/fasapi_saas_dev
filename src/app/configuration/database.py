from sqlmodel import Session, create_engine

from src.app.configuration.settings import settings


DB_USERNAME = settings.db_username
DB_PASSWORD = settings.db_password
DB_HOSTNAME = settings.db_hostname
DB_PORT = settings.db_port
DB_DATABASE = settings.db_database
DB_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"

engine = create_engine(DB_URL)


def get_session():
    with Session(engine) as session:
        yield session
