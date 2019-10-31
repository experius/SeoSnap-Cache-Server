#!/bin/bash

uwsgi --socket 0.0.0.0:5001 --protocol=http -w rendertron_cache_server.wsgi:application
