#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

if [[ $1 == "test" ]]; then
    command docker-compose --env-file ./config/.env.dev up --detach
elif [[ $1 == "prod" ]]; then
    command docker-compose --env-file ./config/.env.prod up --detach
fi
echo -e "\n${bold}Billing server and database server have been run.${normal}\n"