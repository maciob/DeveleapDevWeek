#!/bin/bash
docker network create billing_network

docker build -t billing_server:1.0 app/.
docker run -d --name=flask_server --network=billing_network -p 8080:5000 billing_server:1.0

docker build -t mysql_db:1.0  db/.
docker run -d --name=db_server --network=billing_network -p 8081:3606 mysql_db:1.0
