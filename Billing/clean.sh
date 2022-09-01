#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

docker rm -f mysql-flask-app-container python-flask-app-container

echo -e "\n${bold}Old containers have been cleaned.${normal}\n"
