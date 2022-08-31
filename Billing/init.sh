#!/bin/bash

docker build -t billing_server:1.0 app/.
docker build -t mysql_db:1.0  db/.
echo "done"
