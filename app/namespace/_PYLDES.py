from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class PYLDES(DefinedNamespace):

    # classes
    PageFragmentation: URIRef
    TimeFragmentation: URIRef

    # properties
    alias: URIRef  # alias on which the server hosts a view
    memberFrameSpec: URIRef  # json-ld frame for mapping the LD graph onto JSON-LD objects
    fragmentationKind: URIRef  # kind of pyldes fragmentation applied to a view
    sequenceType: URIRef # denotes the type of the tree:path property on which we want the members to be ordered
    maxNodeSize: URIRef  # node size for page based framentations

    _NS = Namespace("https://pyldes.org/spec/")
