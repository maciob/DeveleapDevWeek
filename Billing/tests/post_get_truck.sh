#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2

curl -i -d "provider=10005" -d "id=789098" -X POST 18.170.241.119:8086/truck | tac | tac | grep -a "200"

if [ $? == 0 ]; then
    echo "Passed when we want to add new truck."
else
    echo "Failed."
fi

curl -i -X GET 18.170.241.119:8086/truck | tac | tac | grep "200"
if [ $? == 0 ]; then
    echo "Passed when we want to get trucks data"
else
    echo "Failed."
fi