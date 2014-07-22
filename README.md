README
=======

An simple app server to save the logs.

Requires
--------

* python-flask
* python-retask

How to run the server?
----------------------

$ python app.py

How to test an upload?
-----------------------

$ curl -F "file=@PATH_TO_THE_LOG_FILE" localhost:5000/

