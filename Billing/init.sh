#!/bin/bash

docker build -t billing_server:1.0 app/.
docker run -d --name=flask_server -v $(pwd)/app/in:/app/in -p 8086:5000 billing_server:1.0

docker build -t mysql_db:1.0  db/.
docker run -d --name=db_server -v $(pwd)/db_volume:/var/lib/mysql -p 8087:3606 mysql_db:1.0

echo "done"
