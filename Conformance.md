Unclear in the spec:
===
Basic behavior
---
 - What should a server root request return?
   Collection & view details -> All data (members) in the LDES collections must be reachable from that information.
   --> not specified nor restricted?

 - What should a request for a view return?
   --> covered by the spec
      
 - What should a request for a node return?
   --> view / viewdescription / collection

Caching
---
 - What caching headers should an immutable fragment be returned with? 
 - 

From the spec
===
Collections
---
 - [SHOULD] Every LDES collection has a Shape specification (SHACL/Shex)
 - [SHOULD] Every LDDES collection has at least one view? [Verify]
   --> Tree collection published via tree:node --> if there is no view then  all memebers should be in the first node
 - []

Views & Nodes
---
 - [MUST] Every member can be reached from a view
 - [SHOULD] Relations have a path property [question] What shoult the path property be for page based fragmentation? -> make sequence explicit so there is order (lessthan, greterthan)
 - [SHOULD] Relations have a value property and the object of tree:value SHOULD be accompanied by a data type when it is a literal value.
 - [MUST] Node has a property linking the current page URL to the URI of the tree:Collection. [remark] This is unclear and examples are lacking. tree:view is a property of a collection, void:subset, dcterms:isPartOf are properties of the node? Are both always needed?
 - [MAY] Multiple view links may be provided
 - [rec] A view description has a dcat:endpointURL  [verify] --> No, this is DCAT compliance, not tree compliance
 - [rec] A view description has a dcat:servesDataset [verify] --> same
 - [MAY] Every tree:Relation MAY provide a tree:remainingItems. A client MAY use tree:remainingItems to estimate the completeness of the downloaded elements to the end-user.

Fragmentation
---
 - Basic fragmentation (fixed sized pages)

 - String based fragmentation

 - Geospatial fragmentation

 - time based fragmentation

Imports
---
 - [MAY/SHOULD] A tree:importStream MAY also be defined for providing a pubsub interface for subscribing to real-time updates. The object SHOULD be a [websockets] or Server-Sent Events ([eventsource]).

Tree Client (out of scope)
---
 - Tree client must traverse all nodes
 - A tree:Node can also be double typed as the tree:ViewDescription. A client must thus check for ViewDescriptions on both the current node without the tree:viewDescription qualification, as on the current node with the tree:viewDescription link
 - TREE client MUST fetch the import of a relation when the relation needs to be correctly evaluated
 - No hypermedia controls in the body MUST be interpreted in imported resources and the object must be fully contained within that information resource.
