#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2

curl -d "username=test_when user does not_exist" -X PUT 18.170.241.119:8086/provider/99 | tac | tac | grep -a "No provider" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed when user does not exist."
else
    echo "Failed."
fi

curl -d "username=test_when user_exists" -X PUT localhost:8086/provider/10001 | tac | tac | grep -a "test_when user_exist" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed when user exists."
else
    echo "Failed."
fi
