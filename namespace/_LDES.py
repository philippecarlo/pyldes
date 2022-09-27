from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef

##
# Created from https://github.com/SEMICeu/LinkedDataEventStreams/blob/master/vocabulary.ttl
##
class LDES(DefinedNamespace):
    
    # classes
    Vocabulary: URIRef
    EventStream: URIRef
    EventSource: URIRef
    RetentionPolicy: URIRef
    LatestVersionSubset: URIRef
    DurationAgoPolicy: URIRef

    # properties
    retentionPolicy: URIRef
    amount: URIRef
    versionKey: URIRef
    versionOfPath: URIRef
    timestampPath: URIRef
    versionMaterializationOf: URIRef
    versionMaterializationUntil: URIRef

    _NS = Namespace("https://w3id.org/ldes#")