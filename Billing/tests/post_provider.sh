#!/bin/bash

pushd ../ > /dev/null
bash -c ./init.sh
popd > /dev/null

sleep 2

curl -d "username=pro1" -X POST localhost:8086/provider | tac | tac | grep -a "already" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi