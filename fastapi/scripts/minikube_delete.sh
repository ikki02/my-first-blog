#!/bin/bash

# 削除
eval $(minikube docker-env -u)
minikube stop
minikube delete
