#!/bin/bash

docker build -t billing_server:1.0 app/.
docker run -d --name=flask_server -p 8000:5000 billing_server:1.0

docker build -t mysql_db:1.0  db/.
docker run -d --name=db_server -p 8001:3606 mysql_db:1.0
