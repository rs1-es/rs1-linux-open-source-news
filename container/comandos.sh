#!/bin/bash

#CADA VEZ QUE LA SESION EXPIRE
aws ecr get-login-password --region eu-west-1 | podman login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com

podman build -t news-rs1-es .
# podman build -t news-rs1-es --no-cache .

#aws ecr create-repository --repository-name news-rs1-es --image-scanning-configuration scanOnPush=true

#CADA VEZ
podman tag news-rs1-es:latest <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com/news-rs1-es:latest

#CADA VEZ, PUEDE VOLVER A PEDIR AUTENTIFICACION
podman push <ACCOUNT_ID>.dkr.ecr.eu-west-1.amazonaws.com/news-rs1-es:latest
