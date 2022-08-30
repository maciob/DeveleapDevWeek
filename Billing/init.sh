#!/bin/bash
docker network create billing_network

docker build -t billing_server:1.0 app/.
docker run -d --name=flask_server  -p 8080:5000 billing_server:1.0

docker build -t mysql_db:1.0  db/.
docker run -d --name=db_server  -p 8081:3606 mysql_db:1.0

sleep 30

docker exec -it db_server mysql -h 127.0.0.1 -u root -ppassword -e "CREATE USER 'app'@'172.17.0.2' IDENTIFIED WITH mysql_native_password BY 'pass';"
docker exec -it db_server mysql -h 127.0.0.1 -u root -ppassword -e "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'app'@'172.17.0.2' WITH GRANT OPTION;"

echo "done"
