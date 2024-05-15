#!/bin/bash

# Stop all running containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -a -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

echo "All Docker containers, images, and volumes have been removed."