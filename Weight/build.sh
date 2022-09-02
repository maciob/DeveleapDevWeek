#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

docker build -t weight_server app-weight/.

echo -e "\n${bold}New images have been built.${normal}\n"
