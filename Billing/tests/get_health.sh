#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2

curl localhost:8086/health | grep -a "OK" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi