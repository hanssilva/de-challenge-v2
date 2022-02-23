# DE Challenge

To solve this challenge I have used the python programming language for its ease and adaptability.
I have created a class, which allows to process the delivered data sources and obtain the requested reports.

# Deploy
For the deployment of the solution my proposal is to use docker. This is one of the most popular ways of hosting scripts and deploying online. Docker can be can use to containerize the code and host it as a microservice using different apps.

## Steps to build docker containes
I also leave this instruccions to deploy on the deployment folder, 
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

# Best practices
- I have tried to use as few lines as possible to solve this problem
- I have used appropriate naming conventions
- I applied the DRY (Don't Repeat Yourself) principle
- I have used Flake8 for Linting (with a max line length of 120)

# Architecture Case
My architecture proposal is in the architecure case folder in which i have used the most reliable and best evaluated open source tools.
