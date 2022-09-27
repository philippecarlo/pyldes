# TODO List

## Caching and proper cache headers: a Functional MUST
Add Flask-Caching support for immutable fragments.

## Write UNIT tests and complete documentation
(prio nr 1)

empty_server_returns_empty_result
collection_without_views_returns_result
non_existing_collection_raises_not_found
non_existing_view_raises_not_found
empty_collection_returns_empty_result

post_existing_collection_raises_invalid_request
post_existing_view_fails_raises_invalid_request
post_view_to_non_existing_collection_raises_invalid_request
post_members_to_non_existing_collection_raises_invalid_request

put_non_existing_collection_raises_not_found
put_non_existing_view_raises_not_found
delete_collection_deleted_views_and_memebers

cache_add_stores_file
cache_get_finds_file
cache_returns_none
cache_lru_works

fragpage_default_request_returns_last_page
fragpage_first_page_contains_no_greater_than
fragpage_page_contains_greater_than
fragpage_page_contains_less_than
fragpage_last_page_contains_no_less_than


## Develop the LDES/TREE conformance tests
(prio nr 2)
--> see conformance tests


## Abstract the models from sqlalchemy
Currently the models for storage are defined in SQLAlachemy only.
It is better to intricuse an abstraction layer and type all operations with it.

## Document the PyLDES namespace (provide spec)
Currently only implicitly defined in the code :-(

## Implement another storage provider
Provide another storage provider e.g., file based.

## Add SHACL shape support and SHACL validation
According to the spec, LDES collections can conform to a provided SHACL shape.
Validation according to this shape can be done using https://github.com/RDFLib/pySHACL

## provide proper logging and tracing and performance monitoring
See https://flask.palletsprojects.com/en/2.2.x/logging/


=============
======== DONE
=============

## Achieve IoC in a proper way for better coupling/cohesion outcome
Use IOC for submodules (e.g., storage provider, pagefragmentation, ...)
See https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html
