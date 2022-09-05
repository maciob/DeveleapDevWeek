#!/bin/bash

# pushd ../ > /dev/null
# command ./init.sh "test"
# popd > /dev/null

# sleep 2
echo " "
echo $0
echo " "
val=1234
curl -i -X GET 18.170.241.119:8086/truck/$val | tac | tac | grep "200" 
if [ $? == 0 ]; then
    echo "Passed."
else
    echo "Failed."
fi