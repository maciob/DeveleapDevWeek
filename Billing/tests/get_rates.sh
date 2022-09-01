#!/bin/bash

pushd ../ > /dev/null
bash -c ./init.sh
popd > /dev/null

sleep 2

curl -i localhost:8086/rates | tac | tac | grep -a "200" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi