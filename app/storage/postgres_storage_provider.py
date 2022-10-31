from typing import List
from sqlalchemy import desc, Integer, DateTime
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from models import Ldes, TreeCollection, TreeView, TreeMember
from rdflib import URIRef
from tools.ldes_server_exception import LdesPresistenceError, LdesNotFoundError, LdesServerError
class PostgresStorageProvider:

    def __init__(self, session_factory, db):
        self.session_factory = session_factory
        self.db = db

    # --- COLLECTIONS / LDES STREAMS --- #
    # to create and update TREE collections (in this case LDES streams)
    def get_ldes_collections(self) -> List[TreeCollection]:
        with self.session_factory() as session:
            all_ldes = session.query(TreeCollection).options(joinedload(TreeCollection.views)).all()
            return all_ldes

    def get_ldes_collection(self, collection_ref: URIRef) -> TreeCollection:
        with self.session_factory() as session:
            try:
                spec = session.query(TreeCollection).options(joinedload(TreeCollection.views)).filter(TreeCollection.id==collection_ref).one()
                return spec
            except SQLAlchemyError as e:
                raise LdesNotFoundError(e)

    def get_ldes_collection_by_alias(self, collection_alias: str) -> TreeCollection:
        with self.session_factory() as session:
            try:
                spec = session.query(TreeCollection).options(joinedload(TreeCollection.views)).filter(TreeCollection.alias==collection_alias).one()
                return spec
            except SQLAlchemyError as e:
                raise LdesNotFoundError(e)            

    def create_ldes_collection(
            self, 
            collection_ref: URIRef, 
            alias: str,
            title: str, 
            member_frame: str) -> TreeCollection:
        with self.session_factory() as session:
            try:
                ldes = Ldes()
                ldes.id = collection_ref
                ldes.alias = alias
                ldes.title = title
                ldes.member_frame = member_frame
                session.add(ldes)
                session.commit()
                session.refresh(ldes)
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)

    def create_or_update_ldes_collection(
            self, 
            collection_ref: URIRef, 
            alias: str, 
            title: str, 
            member_frame: str) -> TreeCollection:
        with self.session_factory() as session:
            try:
                ldes = session.query(TreeCollection).get(collection_ref)
                if not(ldes):
                    ldes = Ldes()
                    ldes.id = collection_ref
                    ldes.alias = alias
                    ldes.title = title
                    ldes.member_frame = member_frame
                    session.add(ldes)
                else:
                    ldes.member_frame = member_frame
                    ldes.title = title
                    ldes.alias = alias
                    session.flush()
                session.commit()
                session.refresh(ldes)
                return ldes
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)
            
    # --- TREE VIEWS --- #
    # to create TREE views on a collection 
    # using some kind of fragmenation or navigation structure
    
    def get_ldes_views(self, collection_ref: URIRef) -> List[TreeView]:
        with self.session_factory() as session:
            if not collection_ref:
                views = session.query(TreeView).all()
                return views
            else:
                views = session.query(TreeView).filter(TreeView.collection_ref == collection_ref).all()
                return views

    def get_ldes_view(self, view_ref: URIRef) -> TreeView:
        with self.session_factory() as session:
            try:
                views = session.query(TreeView).filter(TreeView.id == view_ref).one()
                return views
            except SQLAlchemyError as e:
                raise LdesNotFoundError(e)

    def get_ldes_view_by_alias(self, view_alias: str) -> TreeView:
        with self.session_factory() as session:
            try:
                spec = session.query(TreeView).filter(TreeView.alias==view_alias).one()
                return spec
            except SQLAlchemyError as e:
                raise LdesNotFoundError(e)

    def create_ldes_view(self, 
            collection_ref: URIRef, 
            view_description_ref: URIRef, 
            view_alias: str, 
            fragmentation_kind: URIRef, 
            max_node_size: int,
            path: URIRef,
            sequence_type:str)-> TreeView:
        with self.session_factory() as session:
            try:
                view = TreeView()
                view.collection_id = collection_ref
                view.id = view_description_ref
                view.alias = view_alias
                view.fragmentation_kind = fragmentation_kind
                view.path = path
                view.max_node_size = max_node_size
                view.sequence_type = sequence_type
                session.flush()
                session.commit()
                session.refresh(view)
                return view
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)

    def update_ldes_view(self, 
            collection_ref: URIRef, 
            view_description_ref: URIRef, 
            view_alias: str, 
            fragmentation_kind: URIRef, 
            max_node_size: int,
            path: URIRef,
            sequence_type:str) -> TreeView:
        with self.session_factory() as session:
            try:
                view = session.query(TreeView).get(view_description_ref)
                if not(view):
                    raise LdesNotFoundError(f"Tree view {view_description_ref} does not exist.")
                else:
                    view.collection_id = collection_ref
                    view.alias = view_alias
                    view.fragmentation_kind = fragmentation_kind
                    view.path = path
                    view.max_node_size = max_node_size
                    view.sequence_type = sequence_type
                    session.flush()
                    session.commit()
                    session.refresh(view)
                    return view
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)

    def create_or_update_ldes_view(
            self,
            collection_ref: URIRef, 
            view_description_ref: URIRef, 
            view_alias: str, 
            fragmentation_kind: URIRef, 
            max_node_size: int,
            path: URIRef,
            sequence_type:str):
        with self.session_factory() as session:
            try:
                view = session.query(TreeView).get(view_description_ref)
                if not(view):
                    view = TreeView()
                    view.id = view_description_ref
                    view.collection_id = collection_ref
                    view.alias = view_alias
                    view.fragmentation_kind = fragmentation_kind
                    view.max_node_size = max_node_size
                    view.path = path
                    view.sequence_type = sequence_type
                    session.add(view)
                else:
                    view.collection_id = collection_ref
                    view.fragmentation_kind = fragmentation_kind
                    view.max_node_size = max_node_size
                    view.path = path
                    view.sequence_type = sequence_type
                    session.flush()
                session.commit()
                session.refresh(view)
                return view
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)

    # --- TREE MEMBERS --- #
    # append tree members to a collection

    def add_ldes_member(
            self, 
            collection_ref: URIRef, 
            member_ref: URIRef, 
            member_json: dict, 
            member_rdf: str) -> TreeMember:
        with self.session_factory() as session:
            try:
                m = TreeMember()
                m.id = member_ref
                m.collection_id = collection_ref
                m.json = member_json
                m.rdf = member_rdf
                session.add(m)
                session.commit()
                session.refresh(m)
                return m
            except SQLAlchemyError as e:
                session.rollback()
                raise LdesPresistenceError(e)

    def get_ldes_member_count(self, collection_ref: URIRef) -> int:
        with self.session_factory() as session:
            member_count = session.query(TreeMember).filter(TreeMember.collection_id == collection_ref).count()
            return member_count
    
    def get_ldes_members(self, collection_ref: URIRef, path_ref: URIRef, sequence_type: str, skip: int, take: int) -> List[TreeMember]:
        with self.session_factory() as session:
            if sequence_type == "xsd:int":
                members = session.query(TreeMember)\
                    .filter(TreeMember.collection_id == collection_ref)\
                    .order_by(desc(TreeMember.json[f"{path_ref}"].astext.cast(Integer)))\
                    .offset(skip).limit(take)
                return members
            elif sequence_type == "xsd:dateTime":
                members = session.query(TreeMember)\
                    .filter(TreeMember.collection_id == collection_ref)\
                    .order_by(desc(TreeMember.json[f"{path_ref}"]["@value"].astext.cast(DateTime)))\
                    .offset(skip).limit(take)
                return members
            elif sequence_type == "xsd:string":
                members = session.query(TreeMember)\
                    .filter(TreeMember.collection_id == collection_ref)\
                    .order_by(desc(TreeMember.json[f"{path_ref}"].astext))\
                    .offset(skip).limit(take)
                return members
            else:
                msg = f"Unsupported pyldes:sequence_type '{sequence_type}'"
                raise LdesServerError(msg)

    def storage_ready(self):
        return self.db.db_exists()
    
    def initialize_storage(self):
        self.db.create_database()
    
    def teardown_storage(self):
        self.db.drop_database()