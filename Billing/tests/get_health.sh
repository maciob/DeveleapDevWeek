#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2

curl 18.170.241.119:8086/health | grep -a "OK" &>/dev/null
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi