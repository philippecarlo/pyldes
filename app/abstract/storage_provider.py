from abc import abstractmethod
from typing import List
from rdflib import URIRef

from abstract import AbstractBaseType
from models import Ldes, TreeCollection, TreeView, TreeMember


class StorageProvider(AbstractBaseType):
    """
    An abstract base class for storage providers
    """

    @abstractmethod
    def get_ldes_collections(self) -> List[TreeCollection]:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_collection(self, collection_ref: URIRef) -> TreeCollection:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_collection_by_alias(self, collection_alias: str) -> TreeCollection:
        raise NotImplementedError

    @abstractmethod
    def create_ldes_collection(
            self,
            collection_ref: URIRef,
            alias: str,
            title: str,
            member_frame: str) -> TreeCollection:
        raise NotImplementedError

    @abstractmethod
    def create_or_update_ldes_collection(
            self,
            collection_ref: URIRef,
            alias: str,
            title: str,
            member_frame: str) -> TreeCollection:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_views(self, collection_ref: URIRef) -> List[TreeView]:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_view(self, view_ref: URIRef) -> TreeView:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_view_by_alias(self, view_alias: str) -> TreeView:
        raise NotImplementedError

    @abstractmethod
    def create_ldes_view(self,
                         collection_ref: URIRef,
                         view_description_ref: URIRef,
                         view_alias: str,
                         fragmentation_kind: URIRef,
                         max_node_size: int,
                         path: URIRef,
                         sequence_type: str) -> TreeView:
        raise NotImplementedError

    @abstractmethod
    def update_ldes_view(self,
                         collection_ref: URIRef,
                         view_description_ref: URIRef,
                         view_alias: str,
                         fragmentation_kind: URIRef,
                         max_node_size: int,
                         path: URIRef,
                         sequence_type: str) -> TreeView:
        raise NotImplementedError

    @abstractmethod
    def create_or_update_ldes_view(
            self,
            collection_ref: URIRef,
            view_description_ref: URIRef,
            view_alias: str,
            fragmentation_kind: URIRef,
            max_node_size: int,
            path: URIRef,
            sequence_type: str):
        raise NotImplementedError

    @abstractmethod
    def add_ldes_member(
            self,
            collection_ref: URIRef,
            member_ref: URIRef,
            member_json: dict,
            member_rdf: str) -> TreeMember:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_member_count(self, collection_ref: URIRef) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_ldes_members(self, collection_ref: URIRef, path_ref: URIRef, sequence_type: str, skip: int, take: int) -> List[TreeMember]:
        raise NotImplementedError

    @abstractmethod
    def storage_ready(self):
        raise NotImplementedError

    @abstractmethod
    def initialize_storage(self):
        raise NotImplementedError

    @abstractmethod
    def teardown_storage(self):
        raise NotImplementedError
