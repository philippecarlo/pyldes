from unittest import mock
import pytest
from dependency_injector import providers
from dependency_injector.wiring import inject, Provide

from container import Container
from storage import PostgresStorageProvider, PostgresDB
from models import TreeCollection


tc1 = mock.Mock()
tc1.test_collection_ref = "https://pyldes.org/TestEventStream"
tc1.test_alias = "TestEventStream"
tc1.test_title = "Test EventStream Title"
tc1.test_member_frame = ""

@pytest.fixture
def db():
    db = PostgresDB('postgresql+psycopg2://postgres:postgres@localhost:5432/LDESTEST')
    db.create_database()
    yield db
    db.drop_database()

def test_can_create_collection(db):
    storage = PostgresStorageProvider(db.session)
    storage.create_or_update_ldes_collection(tc1.test_collection_ref, tc1.test_alias, tc1.test_title, tc1.test_member_frame)
    # directly test storage holds the data (do not use get_collection)
    with db.session() as session:
        spec = session.query(TreeCollection).filter(TreeCollection.id==tc1.test_collection_ref).one()
        assert spec is not None

def test_duplicate_alias_throws_error():
    pass

def test_duplicate_alias_throws_error():
    pass

