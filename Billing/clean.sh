#!/bin/bash

docker rm -f flask_server db_server
docker network rm billing_network
