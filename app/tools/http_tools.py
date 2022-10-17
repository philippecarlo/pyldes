from rdflib import Graph, RDF

# cfr https://www.iana.org/assignments/media-types/media-types.xhtml
supported_content_types = [ 'text/n3', 'text/turtle', 'application/ld+json'  ]

def content_type_to_serialization_format(content_type):
        if content_type == 'text/html':
            return 'html' 
        if content_type == 'text/n3': 
            return 'n3' 
        elif content_type == 'text/turtle':
            return 'turtle'
        elif content_type == 'application/ld+json':
            return 'json-ld'
        else:
            return None

def get_content_type(request):
    content_type = request.headers.get('Content-type')
    accept_header = request.headers.get('Accept')
    if accept_header:
        for ct in accept_header.split(','):
            if ct == 'text/html':
                accept_content_type = 'text/html'
                break
            elif ct == 'text/n3':
                accept_content_type = 'text/n3'
                break
            elif ct == 'text/turtle':
                accept_content_type = 'text/turtle'
                break
            elif ct == 'application/ld+json':
                accept_content_type = 'application/ld+json'
                break
            else: #default
                accept_content_type = 'application/ld+json'
    else:
        accept_content_type = 'application/ld+json'
    return content_type, accept_content_type

def parse_data(request_data, content_type):
    parse_format = content_type_to_serialization_format(content_type)
    g = Graph()
    g = g.parse(data=request_data, format=parse_format)
    return g
