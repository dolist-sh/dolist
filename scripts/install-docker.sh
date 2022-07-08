#!/bin/bash

# Script to install docker in the EC2 instance

# https://medium.com/@umairnadeem/deploy-to-aws-using-docker-compose-simple-210d71f43e67

sudo yum update

sudo yum install docker

sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` | sudo tee /usr/local/bin/docker-compose > /dev/null

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

sudo service docker start

exit 0