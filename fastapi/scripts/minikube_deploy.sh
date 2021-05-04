#!/bin/bash

# minikubeのデプロイ
minikube start
eval $(minikube -p minikube docker-env)
sh scripts/docker_build.sh
kubectl apply -f minikube/deployment/dev.yml
#kubectl create deployment myapi --image=myapi:v1 --port=80
kubectl apply -f minikube/service/dev.yml
#kubectl expose deployment myapi --type=LoadBalancer --port=80
minikube service myapi
