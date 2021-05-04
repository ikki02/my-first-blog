#!/bin/bash

#docker run -it --rm -v $(pwd)/:/deploy/ myapi:v1 /bin/bash
docker run -d --rm -p 80:80 --memory=1gb myapi:v1
