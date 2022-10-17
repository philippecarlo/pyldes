import pytest
from unittest import mock
from unittest.mock import Mock

from services import LdesService
from storage import PostgresStorageProvider
from models import TreeCollection

from rdflib import Graph, Literal, URIRef

#region *** Mocks ***
storage_provider = Mock()

collection1 = Mock()
collection1.id = "http://pyldes.org/mock1"
collection1.alias = "MockCollection1" 
collection1.title = "Mock Collection One"
collection1.shape = None
collection1.member_frame = "{}"
view1 = Mock()
view1.id = "http://pyldes.org/mock1/view1"
view1.collection_id = "http://pyldes.org/mock1"
view1.alias = "View1"
view1.fragmentation_kind = "https://pyldes.org/spec/PageFragmentation"
view1.max_node_size = 10
collection1.views = [ view1 ]

collection2 = Mock()
collection2.id = "http://pyldes.org/mock2"
collection2.alias = "MockCollection2"
collection2.title = "Mock Collection Two"
collection2.shape = None
collection2.member_frame = "{}"
view2 = Mock()
view2.id = "http://pyldes.org/mock1/view2"
view2.collection_id = "http://pyldes.org/mock2"
view2.alias = "View2"
view2.fragmentation_kind = "https://pyldes.org/spec/PageFragmentation"
view2.max_node_size = 10
collection2.views = [view2]
#endregion

# some strang mock patching issue generates warnings if using namespace classes
# using plain URIs instead as a workaround
#region *** Mock workaround for RDFLib warnings ***
RDF = Mock()
RDF._ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF.type = URIRef(f"{RDF._ns}type")
LDES = Mock()
LDES._ns = "https://w3id.org/ldes#" 
LDES.EventStream = URIRef(f"{LDES._ns}EventStream")
PYLDES = Mock()
PYLDES._ns = "https://pyldes.org/spec/"
PYLDES.alias = URIRef(f"{PYLDES._ns}alias")
PYLDES.memberFrameSpec = URIRef(f"{PYLDES._ns}memberFrameSpec")
DCTERMS = Mock()
DCTERMS._ns = "http://purl.org/dc/terms/"
DCTERMS.title = URIRef(f"{DCTERMS._ns}title")

#endregion

@pytest.fixture
def ldes_service():
    storage_provider.get_ldes_collections.return_value = [ collection1, collection2 ]
    ldes_service = LdesService(storage_provider, "https://pyldes.org/")
    yield ldes_service


def test_ldes_service_returns_catalog_graph(ldes_service):
    graph = ldes_service.get_ldes_server_catalog()
    # check that the collections
    # (1) are both there
    # (2) each have their view
    # check the realtions for collections and views
    assert (URIRef(collection1.id), RDF.type, LDES.EventStream) in graph
    assert (URIRef(collection1.id), PYLDES.alias, Literal("MockCollection1")) in graph
    assert (URIRef(collection1.id), DCTERMS.title, Literal("Mock Collection One")) in graph
    assert (URIRef(collection1.id), PYLDES.memberFrameSpec, None) in graph

    assert (URIRef(collection2.id), RDF.type, LDES.EventStream) in graph
    assert (URIRef(collection2.id), PYLDES.alias, Literal("MockCollection2")) in graph
    assert (URIRef(collection2.id), DCTERMS.title, Literal("Mock Collection Two")) in graph
    assert (URIRef(collection2.id), PYLDES.memberFrameSpec, None) in graph
