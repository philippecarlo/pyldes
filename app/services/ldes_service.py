import json
from platform import node
from typing import List

from pyld import jsonld
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import DCAT, DCTERMS, DCMITYPE, SOSA, XSD
from namespace import LDES, TREE, PYLDES
from py_linq import Enumerable
from py_linq.exceptions import NoMatchingElement

from dependency_injector.providers import Configuration

from abstract import StorageProvider
from models import TreeCollection, TreeView, TreeMember
from services.page_fragmentation import PageFragmentation
from tools.ldes_server_exception import LdesServerError, LdesNotFoundError


class LdesService:

    '''
    Note: storage provider is resolved using dependency injection.
    Abstract class to be provided later.
    '''

    def __init__(self,
                 storage_provider: StorageProvider,
                 config: Configuration
                 ):
        self.storage_provider = storage_provider
        self.config = config
        self.base_uri = config['ldes']['base_uri']

    '''
    Gets all collections in this server and returns it as an RDF graph.
    '''

    def get_ldes_server_catalog(self) -> Graph:
        graph = self._bind_namespaces(Graph())
        ldes_server = URIRef(self.config['metadata']['server_id'])
        # no def for this in the library :-(
        software = URIRef("http://purl.org/dc/dcmitype/Software")
        graph.add((ldes_server, RDF.type, software))
        for author in self.config['metadata']['authors']:
            graph.add((ldes_server, DCTERMS.creator, Literal(author)))
        graph.add((ldes_server, DCTERMS.hasVersion, Literal(
            self.config['metadata']['major_version'])))

        collections = self.storage_provider.get_ldes_collections()
        for collection in collections:
            self._add_collection_to_graph(graph, collection)
            for view in collection.views:
                self._add_view_description_to_graph(graph, view)

        return graph

    '''
    Gets a single collection using its alias and returns it as an RDF graph.
    '''

    def get_ldes_collection(self, collection_alias: str) -> Graph:
        graph = self._bind_namespaces(Graph())
        ldes = self.storage_provider.get_ldes_collection_by_alias(
            collection_alias)
        self._add_collection_to_graph(graph, ldes)
        return graph

    '''
    Gets a specific LDES view using its alias and returns it as an RDF graph.
    '''

    def get_ldes_view(self, view_alias: str) -> Graph:
        graph = self._bind_namespaces(Graph())
        ldes_view = self.storage_provider.get_ldes_view_by_alias(view_alias)
        self._add_view_description_to_graph(graph, ldes_view)
        return graph

    '''
    Gets a collection node under a view using its id and returns it as an RDF graph.
    If the node id is not specified, it gets the last node of the view
    '''

    def get_ldes_node(
            self,
            collection_alias: str,
            view_alias: str,
            node_id: str) -> Graph:
        graph = self._bind_namespaces(Graph())
        ldes = self.storage_provider.get_ldes_collection_by_alias(
            collection_alias)

        try:
            view = Enumerable(ldes.views).single(
                lambda v: v.alias == view_alias)
        except NoMatchingElement as error:
            raise LdesNotFoundError(
                f"No view found with alias {view_alias} in collection {collection_alias}.")

        self._add_view_description_to_graph(graph, view)
        self._add_collection_to_graph(graph, ldes)

        if not (view.fragmentation_kind) \
                or URIRef(view.fragmentation_kind) == PYLDES.PageFragmentation:
            # resolve with PageFragmentation module
            page_fragmentation = PageFragmentation(
                graph, self.storage_provider, self.base_uri)
            node_id = node_id if node_id else page_fragmentation.get_last_node()
            page_fragmentation.get_node(node_id)
            cacheable = not (page_fragmentation.is_last_node(node_id))
        else:
            raise LdesServerError(
                f"Fragmentation kind specified in view {view.id} is not supported by this server.")
        return graph, cacheable

    '''
    Gets a collection from the storage provider and returns it as TreeCollection model.
    If the node id is not specified, it gets the last node of the view
    '''

    def get_ldes_collection_spec(self, collection_ref: URIRef) -> TreeCollection:
        return self.storage_provider.get_ldes_collection(collection_ref)

    def get_ldes_collection_spec_by_alias(self, alias: URIRef) -> TreeCollection:
        return self.storage_provider.get_ldes_collection_by_alias(alias)

    '''
    Creates an LDES collection or updates it (if it exist)
    '''

    def create_or_update_ldes_collection(
            self,
            graph: Graph,
            collection_ref: URIRef) -> TreeCollection:
        member_frame = graph.value(collection_ref, PYLDES.memberFrameSpec)
        title = graph.value(collection_ref, DCTERMS.title)
        alias = graph.value(collection_ref, PYLDES.alias)
        ldes = self.storage_provider.create_or_update_ldes_collection(
            collection_ref, alias, title, member_frame)
        return ldes

    '''
    Creates an LDES view or updates it (if it exist)
    '''

    def create_or_update_ldes_view(
            self,
            graph: Graph,
            collection_ref: URIRef,
            view_description_ref: URIRef) -> TreeView:
        fragmentation_kind = graph.value(
            view_description_ref, PYLDES.fragmentationKind)
        view_alias = graph.value(view_description_ref, PYLDES.alias)
        max_node_size = graph.value(view_description_ref, PYLDES.maxNodeSize)
        path = graph.value(view_description_ref, TREE.path)
        sequence_type = graph.value(view_description_ref, PYLDES.sequence_type)
        if not sequence_type:
            raise LdesServerError(
                f"A pyldes:sequence_type property denoting the type of the tree:path view property is required.")
        if str(sequence_type) not in ("xsd:string", "xsd:int", "xsd:dateTime"):
            raise LdesServerError(
                f"The provided pyldes:sequence_type {sequence_type} is not supported. Supported types are: 'xsd:string', 'xsd:int', 'xsd:dateTime'.")
        view = self.storage_provider.create_or_update_ldes_view(
            collection_ref, view_description_ref, view_alias, fragmentation_kind, max_node_size, path, sequence_type)
        return view

    '''
    Adds a member to a collection
    '''

    def add_ldes_member(self,
                        graph: Graph,
                        collection_ref: URIRef,
                        member_ref: URIRef) -> TreeMember:
        member_graph = Graph()
        for t in graph.triples((member_ref, None, None)):
            member_graph.add(t)
        # todo: how to identify/get full subgraph?
        member_data = member_graph.serialize(format='turtle')
        member_json = member_graph.serialize(format='json-ld')
        member_doc = json.loads(member_json)
        ldes_spec = self.get_ldes_collection_spec(collection_ref)
        # frame JSON-LD data
        # https://w3c.github.io/json-ld-framing/
        # see also http://blog.sparna.fr/2022/07/20/clean-json-ld-from-rdf-using-framing/
        if ldes_spec.member_frame:
            member_frame = json.loads(ldes_spec.member_frame)
            framed_json = jsonld.frame(member_doc, member_frame)
            # print(framed_json)
            added_member = self.storage_provider.add_ldes_member(
                collection_ref, member_ref, framed_json, member_data)
        else:
            added_member = self.storage_provider.add_ldes_member(
                collection_ref, member_ref, member_doc, member_data)
        return added_member

    '''
    Auxiliary method for adding collection triples to the graph
    '''

    def _add_collection_to_graph(self, graph: Graph, collection: TreeCollection):
        collection_ref = URIRef(collection.id)
        graph.add((collection_ref, RDF.type, LDES.EventStream))
        graph.add((collection_ref, PYLDES.alias, Literal(collection.alias)))
        graph.add((collection_ref, DCTERMS.title, Literal(collection.title)))
        graph.add((collection_ref, PYLDES.memberFrameSpec,
                  Literal(collection.member_frame)))
        return graph

    '''
    Auxiliary method for adding view triples to the graph
    '''

    def _add_view_description_to_graph(self, graph: Graph, view_description: TreeView):
        view_ref = URIRef(view_description.id)
        graph.add((view_ref, RDF.type, TREE.ViewDescription))
        graph.add((view_ref, PYLDES.alias, Literal(view_description.alias)))
        graph.add((view_ref, DCAT.servesDataset,
                  URIRef(view_description.collection_id)))
        if (view_description.fragmentation_kind):
            graph.add((view_ref, PYLDES.fragmentationKind,
                      PYLDES.PageFragmentation))

        if (view_description.path):
            graph.add((view_ref, TREE.path, URIRef(view_description.path)))
        if (view_description.sequence_type):
            graph.add((view_ref, PYLDES.sequence_type,
                      Literal(view_description.sequence_type)))
        if (view_description.max_node_size):
            graph.add((view_ref, PYLDES.maxNodeSize,
                      Literal(view_description.max_node_size)))
        return graph

    '''
    Auxiliary method for creating graph with bound namespaces
    '''

    def _bind_namespaces(self, graph: Graph) -> Graph:
        graph.bind("ldes", LDES)
        graph.bind("tree", TREE)
        graph.bind("dcat", DCAT)
        graph.bind("dcterms", DCTERMS)
        graph.bind("dcmitype", DCMITYPE)
        graph.bind("sosa", SOSA)
        graph.bind("pyldes", PYLDES)
        return graph

    '''
    A method for initializing storage
    '''

    def initialize_storage(self):
        self.storage_provider.initialize_storage()

    '''
    A method for tearing down storage
    '''

    def teardown_storage(self):
        self.storage_provider.teardown_storage()

    '''
    A method for checking if staorage is ready
    '''

    def storage_ready(self):
        return self.storage_provider.storage_ready()
