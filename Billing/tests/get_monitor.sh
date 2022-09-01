#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2

curl localhost:8086/monitor | tac | tac | grep -a "example" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi