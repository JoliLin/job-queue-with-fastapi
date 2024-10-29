sudo docker build -t jq-app .
docker run -d -p 5566:5566 -p 8080:8080 jq-app 
