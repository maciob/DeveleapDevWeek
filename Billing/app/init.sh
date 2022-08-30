#!/bin/bash

docker build -t billing_server:1.0 .
docker run -d --name=flask_server -p 8080:5000 billing_server:1.0