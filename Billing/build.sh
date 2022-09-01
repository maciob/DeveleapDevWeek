#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

docker build -t mysql_db:1.0  db/.
docker build -t billing_server:1.0 app/.

echo -e "\n${bold}New images have been built.${normal}\n"
