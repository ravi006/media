Media Demo
==========

Media is a demo developed to showcase a "search-as-you-type" application
in AngularJS + Flask + Elasticsearch.

Installation
------------

Assumptions:

* Use virtualenv to install Python dependencies

Clone repo, install virtualenv, install Python dependencies::

    cd media
    virtualenv env
    source ./env/bin/activate
    pip install -r requirements.txt

Create basic database (use data from `data/media.data`)::

    make index

Run backend service::

    make backend

Run frontend service::

    make frontend

Point your browser to::

    http://localhost:8000



