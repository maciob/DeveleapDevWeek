#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2
echo " "
echo $0
echo " "
curl 18.170.241.119:8086/health | grep -a "OK" 
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi