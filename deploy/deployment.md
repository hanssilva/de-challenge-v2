# Deploy
For the deployment of the solution my proposal is to use docker. This is one of the most popular ways of hosting scripts and deploying online. Docker can be can use to containerize the code and host it as a microservice using different apps.

## Steps to build docker containes
To create a new deploy, on your folder you must run:
```sh
# Build docker image
(DE-CHALLENGE-V2) $ docker build -t etl:0.0.1

# Delete previous container if exist
(DE-CHALLENGE-V2) $ docker rm etl

# Create and run container
(DE-CHALLENGE-V2) $ docker run --name etl etl:0.0.1

# If you want to run it again
(DE-CHALLENGE-V2) $ docker start -a etl
```