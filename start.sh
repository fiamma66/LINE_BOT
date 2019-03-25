#!/bin/bash

docker volume create portainer_data

echo "====create portainer======="

create_portainer()
{
docker run -d -p 9000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer

}
if [[ `docker ps -a | grep portainer | wc -l` = 0 ]]; then
  create_portainer

else 
  docker stop portainer
  docker rm -f portainer
  create_portainer
fi


create_docker_compose()
{
docker-compose up -d --build
}

if [[ `docker images | grep fiamma66/line_bot_jupyter | wc -l` = 0 ]]; then
  create_docker_compose
else
  docker-compose up -d
fi


sleep 4



echo "==============="
echo ""
curl -s "localhost:4040/api/tunnels" | awk -F',' '{print $3}' | awk -F'"' '{print $4}' | awk -F'//' '{print $2}'
echo ""
echo "==============="




