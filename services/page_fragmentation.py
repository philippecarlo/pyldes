import os
from rdflib import Graph, BNode, Literal, RDF, URIRef
from namespace import LDES, TREE, PYLDES
from py_linq import Enumerable
from tools.ldes_server_exception import LdesServerError

DEFAULT_MAX_NODE_SIZE = 100

class PageFragmentation:
    '''
    The PageFragmentation class is initialized using a Graph containing 
    the necessary collection and view triples.
    Todo: identify a PageFragmentation interface and extract an abstract class.
    Note: the storage provider is injected, abstract class to be defined
    '''
    def __init__(self, graph: Graph, storage_provider, base_uri: str):
        self.storage_provider = storage_provider
        self.base_uri = base_uri
        self.graph = graph
        self.collection_ref = Enumerable(self.graph.subjects(RDF.type, LDES.EventStream)).single()
        self.collection_alias = Enumerable(self.graph.objects(self.collection_ref, PYLDES.alias)).single()
        if not(self.collection_ref):
            raise LdesServerError("Internal error: No collection specification passed to PageFragmentation module.")
        self.view_description_ref = Enumerable(self.graph.subjects(RDF.type, TREE.ViewDescription)).single()
        self.view_alias = Enumerable(self.graph.objects(self.view_description_ref, PYLDES.alias)).single()
        if not(self.view_description_ref):
            raise LdesServerError("Internal error: No view description passed to PageFragmentation module.")
        self.max_node_size = int(self.graph.value(self.view_description_ref, PYLDES.maxNodeSize))
        if not(self.max_node_size):
            self.max_node_size = DEFAULT_MAX_NODE_SIZE

    '''
    Gets a view node and returns it as a graph.
    '''
    def get_node(self, node_id) -> Graph:
        last_node = self.get_last_node()
        node_id = last_node if not node_id else int(node_id)
        node_ref = URIRef(f"{self.base_uri}/ldes/{self.collection_alias}/{self.view_alias}?node={node_id}")
        self.graph.add((node_ref, RDF.type, TREE.Node))
        self.graph.add((node_ref, TREE.viewDescription, self.view_description_ref))
        

        if not(node_id == last_node):
            previous_relation = BNode()
            self.graph.add((previous_relation, RDF.type, TREE.GreaterThanRelation))
            self.graph.add((previous_relation, TREE.node, URIRef(f"{self.base_uri}/ldes/{self.collection_alias}/{self.view_alias}?node={node_id+1}")))
            self.graph.add((previous_relation, TREE.value, Literal(node_id+1)))
            self.graph.add((node_ref, TREE.relation, previous_relation))

        if node_id > 1:
            next_relation = BNode()
            self.graph.add((next_relation, RDF.type, TREE.LessThanRelation))
            self.graph.add((next_relation, TREE.node, URIRef(f"{self.base_uri}/ldes/{self.collection_alias}/{self.view_alias}?node={node_id-1}")))
            self.graph.add((next_relation, TREE.value, Literal(node_id-1)))
            self.graph.add((node_ref, TREE.relation, next_relation))

        self._add_node_memebers(node_id)
        return self.graph
    
    '''
    Auxiliary function to add members to a node graph.
    '''
    def _add_node_memebers(self, node_id):
        skip = (node_id -1) * self.max_node_size
        members = self.storage_provider.get_ldes_members(self.collection_ref, skip, self.max_node_size)
        buffer = str()
        for member in members:
            self.graph.add((self.collection_ref, TREE.member, URIRef(member.id)))
            buffer += member.rdf
            buffer += os.linesep
        self.graph.parse(data=buffer, format="turtle")

    '''
    Checks if the current node is the last one.
    '''
    def is_last_node(self, node_id) -> bool:
        last_node_id = self.get_last_node()
        return f"{node_id}" == f"{last_node_id}"

    '''
    Resolves the last node of the view (i.e., the one that can still change)
    '''
    def get_last_node(self):
        member_count = self.storage_provider.get_ldes_member_count(self.collection_ref)
        nr_of_full_nodes = member_count // self.max_node_size
        remainder_members = member_count % self.max_node_size
        last_node = nr_of_full_nodes if remainder_members == 0 else nr_of_full_nodes +1
        return last_node
