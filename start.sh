#!/bin/bash

docker volume create portainer_data

echo "====create portainer======="
docker run -d -p 9000:9000 --rm --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer

docker-compose up -d --build


sleep 4



echo "==============="
echo ""
curl -s "localhost:4040/api/tunnels" | awk -F',' '{print $3}' | awk -F'"' '{print $4}' | awk -F'//' '{print $2}'
echo ""
echo "==============="




