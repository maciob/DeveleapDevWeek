#!/bin/bash

pushd ../ > /dev/null
bash -c ./init.sh
popd > /dev/null

sleep 5

curl -d "username=test_when user doesnt_exist" -X PUT localhost:8086/provider/99 | tac | tac | grep -a "No provider" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed when user doesnt exist."
else
    echo "Failed."
fi

curl -d "username=test_when user_exist" -X PUT localhost:8086/provider/10001 | tac | tac | grep -a "test_when user_exist" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed when user exist."
else
    echo "Failed."
fi
