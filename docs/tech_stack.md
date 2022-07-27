# Tech stack to be used

- FastAPI backend
- Azure SQL database
- Azure App service

## Fast API

Fast API is a web framework for developing APIs in python

Resons to use FastAPI:

- #### _Performance_ 

FastAPI is much faster than flask and has performance on par with node.js and go.

- #### _Asynchronous Support_

FastAPI is built over ASGI as oppsed to WSGI, this gives it asynchronous support.

- #### _Ease of use_

FastAPI has a comprehensive documentation and makes use typed python. It also has a simple inferface and an API can be set up with minimal code.

- #### _Automatic Documentation_

FastAPI generated Swagger documentation automatically without the need for additional code.


## Azure SQL database

Azure SQL database is a fully managed database service.
It is sclable and does not require additional overhead to maintain.

## Azure App service

- Azure App service is a serverless compute service
- It is easier to set up than a kubernetes cluster and for a single API like this is a better approach.
- It has built in CI/CD support
- It provides capability to create multiple environments and split traffic between them.
- Autoscalling can also be configured