docker run -d -p 5000:5000 --restart=always --name registry registry:2

docker tag connect-four localhost:5000/connect-four
docker push localhost:5000/connect-four

curl http://localhost:5000/v2/_catalog