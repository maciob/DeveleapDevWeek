#!/bin/bash
docker rm -f $(docker ps -aq)
docker build . -t trackerservice:1.0
docker run --name tracker -itd -p 8089:5000 -v $(pwd)/../../../testing:/app/git trackerservice:1.0


