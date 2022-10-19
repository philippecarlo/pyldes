import sqlalchemy as sa 
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.functions import database_exists
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from models.tree_base import Base
import logging

logger = logging.getLogger(__name__)

class PostgresDB:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False) # change to echo=True for logging
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                expire_on_commit=False, #important for using objects after detach
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )
    
    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)
    
    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as ex:
            logger.exception(f"Session rollback because of exception. {str(ex)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_database(self):
        Base.metadata.create_all(self._engine)

    def drop_database(self):
        Base.metadata.drop_all(self._engine)
    
    def db_exists(self):
        if database_exists(self._engine.url):
            insp = sa.inspect(self._engine)
            table_present = insp.has_table("TreeCollection", schema="public")
            return table_present
        else:
            return False
