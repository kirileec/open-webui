
from contextlib import contextmanager

from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from open_webui.env_linx import SSO_DB_URL, SSO_SQL


if SSO_SQL!='':
    engine2 = create_engine(
        SSO_DB_URL,pool_pre_ping=True, pool_recycle=3600, poolclass=NullPool,echo=True
    )
    SessionLocal2 = sessionmaker(bind=engine2,autocommit=False,autoflush=False,expire_on_commit=False)
    Session2 = scoped_session(SessionLocal2)
    def get_session2():
        db2 = SessionLocal2()
        try:
            yield db2
        finally:
            db2.close()
    get_db2 = contextmanager(get_session2)