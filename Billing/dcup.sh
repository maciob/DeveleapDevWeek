#!/bin/bash

if [[ $1 == "test" ]]; then
    command docker-compose --env-file ./config/.env.dev up --detach
elif [[ $1 == "prod" ]]; then
    command docker-compose --env-file ./config/.env.prod up --detach
fi
echo "Done."