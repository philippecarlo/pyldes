# pyldes

A Python LDES Server

## Introduction

This Linked Data Event Stream server is developed with the purpose to create an LDES conformance 
testing suite. It implements the [LDES specification](https://semiceu.github.io/LinkedDataEventStreams/) which is based itself on the [TREE Hypermedia Specification](https://treecg.github.io/specification/).

## Conformance
The conformance tests can be found under the [Conformance](app/Conformance) folder in this repository.

## Running and testing

### Local Setup
The easiest way to configure your local setup is via the Make actions executed from within the [app](app) directory of 
this project.

#### To check the supported Make actions
```shell
make 
```
or
```shell
make help
```
#### Activate a Python virtual environment and install the application dependencies
```shell
make build
```
#### To start a Pyldes locally
This will only start the Pyldes service. It is expected that a local or dockerized Postgres service already is 
deployed.
```shell
make run
```
#### To clean the local build environment
```shell
make clean
```

### Dependencies

The PyLDES server is a Flask based LDES server written in Python3.
Before running, check the dependency list in the [requirements.txt](app/requirements.txt) file.

One can install the dependencies listed in the requirements.txt file via:
```
pip3 install -r requirements.txt
```
or by building the local environment as described in [Local Setup](#local-setup)

Running with socket support also requires gunicorn. This is also part of the requirements.txt file and
will be deployed together with the other application dependencies.

### Docker
Before one build the Docker containers one needs to check if the configuration values in [pyldes.env](pyldes.env)
are correctly set.

In the [docker-compose.yml](docker-compose.yml) one can see that following Dockers containers will be build
and launched based on the given Make action.
* Pyldes
* Postgres

The below listed Make actions need to be executed from within the root of the project.
This [Makefile](Makefile) has a dependency on the [pyldes.env](pyldes.env) configuration file and the 
[Makefile](app/Makefile) from the [app](app) directory

#### To check the supported Make actions
```shell
make 
```
or
```shell
make help
```
#### To build the Docker containers
This action will automatically remove (if exists) the Python virtual environment from with the [app](app) folder.
```shell
make build
```
#### To run the Docker containers
```shell
make run
```
#### To stop the Docker containers
```shell
make stop
```

### PostgreSQL

The PyLDES server was developed using PostgreSQL version 12 but any reasonably
recent version should do. All that is needed is to spin it up, create a DB with
proper privileges and configure the endpoint URL: ```postgres_url``` in the [config.yml](/app/config.yml) file.

To use the service, you need to seed the database using the following command:

```shell
curl --request GET \
  --url http://localhost:5000/manage/init
```
After executing the above request, the server should be accessible at the root location. By default, the server hosts an endpoint on localhost port 5000. Browsing to it with a browser will show the empty server page. Querying the root address with a HTTP client (e.g., insomnia or postman) will result in the basic server information being returned. 

### Creating a collection

```shell
curl --request POST \
  --url http://localhost:5000/ldes \
  --header 'Accept: text/turtle' \
  --header 'Content-Type: text/turtle' \
  --data 'BASE   <https://pyldes.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tree: <https://w3id.org/tree#>
PREFIX ldes: <https://w3id.org/ldes#>
PREFIX pyldes: <https://pyldes.org/spec/>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dcterms: <http://purl.org/dc/terms/>

<https://data.imec.be/cityflows> a ldes:EventStream;
	pyldes:alias "Cityflows";
  dcterms:title "A sample event stream with some basic cityflows members.";
	pyldes:memberFrameSpec "{ \"@type\":\"http://www.w3.org/ns/sosa/Observation\", \"http://www.w3.org/ns/sosa/resultTime\": {}, \"http://www.w3.org/ns/sosa/madeBySensor\": {}, \"http://www.w3.org/ns/sosa/observedProperty\": {}, \"http://www.w3.org/ns/sosa/hasSimpleResult\":{}}".

<CityflowsDefaultView>
  a tree:ViewDescription;
	pyldes:alias "CityflowsDefaultView";
	dcat:servesDataset <https://data.imec.be/cityflows>;
	tree:path sosa:resultTime;
	pyldes:fragmentationKind pyldes:PageFragmentation;
	pyldes:maxNodeSize "100"^^xsd:int;
	pyldes:sequence_type "xsd:dateTime".
  '
```
Some notes apply to this snippet. 
1. The `pyldes:memberFrameSpec` property is used to map the graph representation of a member to a non-graph json snippet used by the Postgres storage component. This is not part of the specification and may be obsoleted later when SHACL-support is added.
2. The `pyldes:fragmentationKind` is a built-in fragmentation of this server that is provided for convenience and is not part of the specification. The same applies to `pyldes:maxNodeSize`. 
3. The `pyldes:sequence_type` is currently needed for the fragmentation to understand how it should order the data.  It may be osoleted when SHACL support is added.

After creating the collection and the view, it shows in the root request and it is possible to follow the link to the view. The response will be empty.

### Adding memebers
The following command can be used to add a member. It is possible to add multiple members in batch.
Take note that using this method to add members (currently) requires to specify the meber type as an argument to the request.

```shell
curl --request POST \
  --url http://localhost:5000/ldes/Cityflows?member_type=http://www.w3.org/ns/sosa/Observation \
  --header 'Accept: text/turtle' \
  --header 'Content-Type: text/turtle' \
  --data 'BASE   <https://pyldes.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX tree: <https://w3id.org/tree#>
PREFIX ldes: <https://w3id.org/ldes#>
PREFIX pyldes: <https://pyldes.org/spec/>
PREFIX sosa: <http://www.w3.org/ns/sosa/>

<https://data.imec.be/cityflows/cropland/schoolstraat/123456789> a sosa:Observation ;
    sosa:hasSimpleResult 3.55339e+03 ;
		sosa:resultTime "2022-11-24T08:00:00+00:00"^^xsd:dateTime ;
    sosa:madeBySensor <https://data.imec.be/cityflows/cropland/schoolstraat/unknown> .
  '
  ```
