# pyldes
A Python LDES Server

## Introduction
(todo)

## Conformance
(todo)


## Requirements
(todo)


## Running en testing

### Dependencies

The PyLDES server is a Flask based LDES server written in Python3.
Before running, check the dependency list in the Requirements.txt file.
You can install them using the following command:
```
$ pip3 install -r requirements.txt
```
Running with socket support also requires guinicorn. Make sure to install it first.

### PostgreSQL

The PyLDES server was developed using PostgreSQL version 12 but any reasonably 
recent version should do. All that is needed is to spin it up, create a DB with 
proper privileges and configure the endpoint URL in the config.yml file.

### running

Running the server can be done from the root directory as follows:
```
$ gunicorn -k eventlet -w1 --timeout 6000 server:app
```

### using
The server hosts an endpoint on localhst port 5000.
You can point your browser to it or do a get request using nay HTTP client.
You can follow the LDES/TREE links from there ;-).