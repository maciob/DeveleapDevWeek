#!/bin/bash

pushd ../ > /dev/null
command ./init.sh "test"
popd > /dev/null

sleep 2

curl -X POST localhost:8086/rates | tac | tac | grep "successfully" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi