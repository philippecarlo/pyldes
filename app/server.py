#!/usr/bin/env python
# encoding: utf-8

# 3rd party libs
import traceback, time
from zipapp import create_archive
from flask import Flask, redirect, request, g
from flask_socketio import SocketIO
from werkzeug.serving import WSGIRequestHandler
from rdflib import Graph, RDF
from rdflib.namespace import DCAT
from dependency_injector.wiring import inject, Provide
from dependency_injector.providers import Configuration

# LDES server modules
from services.ldes_service import LdesService
from container import Container
from storage import PostgresStorageProvider
from storage.postgres_db import PostgresDB
from namespace import LDES, TREE

# tools and instrumentation
from tools.ldes_2_html import render_ldes_server, render_ldes_node, render_ldes_socket_demo
from tools.ldes_cache import LdesCache
from tools.ldes_server_exception import LdesNotFoundError, LdesServerError
from tools.bcolors import bcolors
from tools.http_tools import get_content_type, content_type_to_serialization_format, parse_data

app = Flask(__name__)
@app.route('/')
def index():
    return redirect("/ldes", code=302)

@app.route('/ldes', methods = ['GET'])
@inject
def ldes(ldes_service: LdesService = Provide[Container.ldes_service]):
    content_type, accept_type = get_content_type(request)
    serialization_format = content_type_to_serialization_format(accept_type)

    storage_ready = ldes_service.storage_ready()
    if not storage_ready:
        if serialization_format == "html":
            return render_ldes_server(None)
        else:
            raise LdesServerError(f"Storage not initialized. Initialize it first with the /manage/init endpoint.")

    data = ldes_service.get_ldes_server_catalog()
    if serialization_format == "html":
        return render_ldes_server(data)
    else:
        return data.serialize(format=serialization_format), 200, {'Content-Type': accept_type }

@app.route('/ldes/<collection_alias>/<view_alias>', methods = ['GET'])
@inject
def get_ldes(
    collection_alias: str, 
    view_alias: str, 
    ldes_service: LdesService = Provide[Container.ldes_service], 
    ldes_cache: LdesCache = Provide[Container.ldes_cache]):

    # Since LDES fragments are immutable we always return 304 to indicate the 
    # cached copy can be used when an if-none-match header is passed.
    client_etag = request.headers.get('If-None-Match')
    if client_etag and client_etag in ldes_cache.mem_cache.keys():
        return "", 304
    content_type, accept_type = get_content_type(request)
    serialization_format = content_type_to_serialization_format(accept_type)

    try:
        if request.method == 'GET':
            cacheable = False
            cache_key = None
            node_id = request.args.get('node')
            if node_id is not None:
                cache_key = f"{collection_alias}-{view_alias}-{node_id}"
                serialized_data = ldes_cache.get(cache_key)
                if serialized_data:
                    data = Graph()
                    data.parse(data=serialized_data, format="turtle")
                    cacheable = True
                else:
                    data, cacheable = ldes_service.get_ldes_node(collection_alias, view_alias, node_id)
                    if cacheable:
                        serialized_data = data.serialize(format="turtle")
                        ldes_cache.put(cache_key, serialized_data)
            else:
                # by the spec this resolves to the last (mutable) node, so no caching
                data, cacheable = ldes_service.get_ldes_node(collection_alias, view_alias, node_id=None)

            headers = dict()
            headers['Content-Type'] = accept_type
            headers['Cache-Control'] = "max-age=31536000" if cacheable else "max-age=10"
            if cacheable:
                headers['ETag'] = cache_key

            if serialization_format == "html":
                response = render_ldes_node(data)
                return response, 200, headers
            else:
                return data.serialize(format=serialization_format), 200, headers
        else:
            return ('Method not supported', 400) 
    except LdesNotFoundError as error:
        message = error.message if hasattr(error, 'message') else ''
        return (message, 404)
    except LdesServerError as error:
        message = error.message if hasattr(error, 'message') else ''
        return (message, 500)

@app.route('/ldes', methods = ['POST'])
@inject
def post(ldes_service: LdesService = Provide[Container.ldes_service], config: Configuration = Provide[Container.config]):
    storage_ready = ldes_service.storage_ready()
    if not storage_ready:
        raise LdesServerError(f"Storage not initialized. Initialize it first with the /manage/init endpoint.")

    content_type, accept_type = get_content_type(request)
    serialization_format = content_type_to_serialization_format(accept_type)
    graph = None

    # step 0: check for valid RDF data if data is submitted
    if request.data:
        try:
            graph = parse_data(request.data, content_type)
        except Exception as ex1:
            return f'Failed to parse data: {str(ex1)}', 400, {'Content-Type': 'text/plain' }

    # step 1: create or update the LDES collection
    for collection_ref, _, __ in graph.triples((None, RDF.type, LDES.EventStream)):
        try:
            ldes = ldes_service.create_or_update_ldes_collection(graph, collection_ref)
            ldes_graph = ldes_service.get_ldes_collection(ldes.alias)
            app.socket_io_app.emit("tree:collection", ldes_graph.serialize(format='turtle'), json=False, broadcast=True)
        except Exception as ex2:
            traceback.print_exc()
            return (f'Failed to create LDES: {str(ex2)}', 400, {'Content-Type': 'text/plain' })
    
    # step 2: if the data contains view definitions, then add the views
    for view_descr_ref, __, _  in graph.triples((None, RDF.type, TREE.ViewDescription)):
        try:
            collection_ref = graph.value(view_descr_ref, DCAT.servesDataset)
            ldes_view = ldes_service.create_or_update_ldes_view(graph, collection_ref, view_descr_ref)
            ldes_graph = ldes_service.get_ldes_view(ldes_view.alias)
            app.socket_io_app.emit("tree:view", ldes_graph.serialize(format='turtle'), json=False, broadcast=True)
        except Exception as ex3:
            traceback.print_exc()
            return (f'Failed to process view description: {str(ex3)}', 400, {'Content-Type': 'text/plain' })

    # step 3: if the data contains members for a collection add these members
    # for collection_ref, __, member_ref  in graph.triples((None, TREE.member, None)):
    # turned the relation around (currently not supported in TREE)
    for member_ref, __, collection_ref  in graph.triples((None, TREE.memberOf, None)):
        try:
            added_member = ldes_service.add_ldes_member(graph, collection_ref, member_ref)
            app.socket_io_app.emit("tree:member", added_member.rdf, json=False, broadcast=True)
        except Exception as ex4:
            traceback.print_exc()
            return (f'Failed to process LDES member: {str(ex4)}', 400, {'Content-Type': 'text/plain' })

    # finally: return the result collection along with views
    return '', 204, {'Content-Type': accept_type }

@app.route('/manage/init')
@inject
def init(ldes_service: LdesService = Provide[Container.ldes_service]):
    ldes_service.initialize_storage()
    return ('', 204)

@app.route('/manage/teardown')
@inject
def teardown(ldes_service: LdesService = Provide[Container.ldes_service], ldes_cache: LdesCache = Provide[Container.ldes_cache]):
    ldes_service.teardown_storage()
    ldes_cache.clear()
    return ('', 204)

@app.route('/socketdemo')
def socket_demo():
    return render_ldes_socket_demo(), 200


'''
Registering event handlers and starting the app
'''
@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    print (f"--> Request execution time {bcolors.UNDERLINE}{diff}{bcolors.ENDC}s.")
    return response


app.container = Container()
app.debug = app.container.config.flask.debug() == "true"
app.send_file_max_age_default = int(app.container.config.flask.send_file_max_age_default())
app.container.wire(modules=[__name__])
WSGIRequestHandler.protocol_version = "HTTP/1.1"
print(bcolors.CYAN)
with open("logo.txt", 'r') as fin:
    print(fin.read())
print(bcolors.ENDC)
app.socket_io_app = SocketIO(app, cors_allowed_origins="*", engineio_logger=True)

# run with sufficiently large timeout to prevent socket from killing the workers:
# gunicorn -k eventlet -w1 --timeout 6000 server:app

if __name__ == "__main__":
    app.socket_io_app.run(app)

