#!/bin/bash

pushd ../ > /dev/null
bash -c ./init.sh
popd > /dev/null

sleep 2

curl localhost:8086/health | grep "OK" &> /dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi