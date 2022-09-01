#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

if [ $# -eq 0 ]; then
    echo "Provide an argument -- 'test' for test environment or 'prod' for production environment"
else
    ./clean.sh
    ./build.sh
    ./dcup.sh $1
fi

echo -e "\n${bold}Billing app initialization completed.${normal}\n"