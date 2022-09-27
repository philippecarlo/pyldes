from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef

###
# created from https://github.com/TREEcg/specification/blob/master/tree.ttl
##
class TREE(DefinedNamespace):
    
    # classes
    Collection: URIRef
    ViewDescription: URIRef
    Node: URIRef
    Relation: URIRef
    ConditionalImport: URIRef
    PrefixRelation: URIRef
    SubstringRelation: URIRef
    SuffixRelation: URIRef
    GreaterThanRelation: URIRef
    GreaterThanOrEqualToRelation: URIRef
    LessThanRelation: URIRef
    LessThanOrEqualToRelation: URIRef
    EqualToRelation: URIRef
    GeospatiallyContainsRelation: URIRef
    InBetweenRelation: URIRef

    ######## Properties
    viewDescription: URIRef
    relation: URIRef
    remainingItems: URIRef
    node: URIRef
    value: URIRef
    path: URIRef
    view: URIRef
    member: URIRef
    memberOf: URIRef
    search: URIRef
    shape: URIRef
    _import: URIRef
    conditionalImport: URIRef
     
    ###### Properties for the Tiles ontology
    zoom: URIRef
    longitudeTile: URIRef
    latitudeTile: URIRef
    timeQuery: URIRef

    _NS = Namespace("https://w3id.org/tree#")