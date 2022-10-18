
import json
from pyld import jsonld
from rdflib import Graph
from flask import render_template

def render_ldes_server(data: Graph):
    if data is None:
        return render_template('ldes_server.html', title='Linked Data Event Stream Server', model=None, message='Storage not initialized, initialize it first.')
    _json = data.serialize(format='json-ld')
    _frame = { 
        "@context": { "https://w3id.org/tree#view": { "@reverse" : "http://www.w3.org/ns/dcat#servesDataset" } },
        "@type": "https://w3id.org/ldes#EventStream",
        "https://w3id.org/tree#view" : {
            "@type" : "https://w3id.org/tree#ViewDescription"
        }
    }
    server_details_graph = jsonld.frame(json.loads(_json), _frame)
    collections = [ server_details_graph]  if not("@graph" in server_details_graph.keys()) else server_details_graph["@graph"]
    # ensure views is a list
    # this is a bit ugly, I admit but I could not figure out how to solve this differently
    # JSONLD framing does not make a list of views when there is one view only
    # and I found no way of enforcing that
    for collection in collections:
        if not isinstance(collection['https://w3id.org/tree#view'], list):
            view = collection['https://w3id.org/tree#view']
            collection['https://w3id.org/tree#view'] = [view]
    
    return render_template('ldes_server.html', title='Linked Data Event Stream Server', model=collections)
    
def render_ldes_node(data: Graph):
    _json = data.serialize(format='json-ld')
    _frame = { "@type" : "https://w3id.org/tree#Node"  }
    ldes_node = jsonld.frame(json.loads(_json), _frame)
    # same issue as with views above, need to ensure relations is a list
    if 'https://w3id.org/tree#relation' not in ldes_node.keys():
        ldes_node['https://w3id.org/tree#relation'] = []
    if not isinstance(ldes_node['https://w3id.org/tree#relation'], list):
        relation = ldes_node['https://w3id.org/tree#relation']
        ldes_node['https://w3id.org/tree#relation'] = [ relation ]
    #print(ldes_node)
    return render_template('ldes_node.html', title='Linked Data Event Stream Server', model=ldes_node, json=json)

def render_ldes_collection(data: Graph):
    #todo: should resolve to render_ldes_node
    pass

def render_ldes_socket_demo():
    return render_template('ldes_socket_demo.html', title='Linked Data Event Socket', model=None, json=json)