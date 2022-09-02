#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2
echo " "
echo $0
echo " "
curl -d "username=pro1" -X POST 18.170.241.119:8086/provider | tac | tac | grep -a "already" 
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi