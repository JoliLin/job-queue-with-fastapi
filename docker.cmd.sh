BACK_IMAGE=jq.backend
BACK_CONTAINER=jq.back
FRONT_IMAGE=jq.frontend
FRONT_CONTAINER=jq.front

sudo docker build --target app1 -t $BACK_IMAGE .
sudo docker build --target app2 -t $FRONT_IMAGE .

source .env
sudo docker run -d -p $BACK_PORT:$BACK_PORT --env-file .env --name $BACK_CONTAINER $BACK_IMAGE 
sudo docker run -d -p $WEB_PORT:$WEB_PORT --env-file .env --name $FRONT_CONTAINER $FRONT_IMAGE
