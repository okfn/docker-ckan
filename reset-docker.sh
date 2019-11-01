docker-compose down

docker rm $(docker ps -a -f status=exited -f status=created -q)

docker images -q |xargs docker rmi
docker rmi $(docker images -f dangling=true -q)      
docker rmi $(docker images -q)    

docker image prune -a
