#!/bin/bash

docker build -t mysql_db:1.0  db/.
docker build -t billing_server:1.0 app/.

echo "Done."