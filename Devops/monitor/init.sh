#!/bin/bash
#docker rm -f $(docker ps -aq)
docker build . -t monitorservice:1.0
docker run --name monitor -itd -p 8088:5000 monitorservice:1.0


