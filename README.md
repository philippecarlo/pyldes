# pyldes

A Python LDES Server

## Introduction

(todo)

## Conformance

(todo)

## Requirements

(todo)

## Running en testing

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
* Postgress

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
proper privileges and configure the endpoint URL in the config.yml file.

To use the service, you need to seed the database using the following command:

```shell
curl --request GET \
  --url http://localhost:5000/manage/init
```

At this time, the service also requires that at least one collection is created in storage:

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

<https://pyldes.org/SampleEventStream> a ldes:EventStream;
  pyldes:alias "SampleEventStream";
  dcterms:title "A sample Event Stream with Bogus data";
  pyldes:memberFrameSpec "{ \"@type\":\"http://www.w3.org/ns/sosa/Observation\", \"http://www.w3.org/ns/sosa/madeBySensor\": {}, \"http://www.w3.org/ns/sosa/hasSimpleResult\":{}}";
  tree:member <SampleMember1>, <SampleMember2>, <SampleMember3>, <SampleMember4>, <SampleMember5>, <SampleMember6>, <SampleMember7>, <SampleMember8>, <SampleMember9>, <SampleMember10> .

<SampleMember1> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "121"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember2> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "122"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember3> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "123"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember4> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "124"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember5> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "125"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember6> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "126"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember7> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "127"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember8> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "128"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember9> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "129"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .

<SampleMember10> a sosa:Observation;
  sosa:madeBySensor <bogusSensor>;
  sosa:hasSimpleResult "130"^^xsd:float;
  tree:memberOf <https://pyldes.org/SampleEventStream> .


<SamplePageSizeView>
  a tree:ViewDescription;
  pyldes:alias "SampleView";
  dcat:servesDataset <https://pyldes.org/SampleEventStream>;
  pyldes:fragmentationKind pyldes:PageFragmentation;
  pyldes:maxNodeSize "4"^^xsd:int.



  '
```

### using

The server hosts an endpoint on localhost port 5000.
You can point your browser to it or do a get request using any HTTP client.
You can follow the LDES/TREE links from there ;-).