#!/bin/bash
#docker  rm #asd-f $(docker ps -aq)
docker build . -t trackerservice:1.0
docker run --name tracker -itd -p 8089:5000 -v /var/run/docker.sock:/var/run/docker.sock trackerservice:1.0


