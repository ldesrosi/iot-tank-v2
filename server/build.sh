#! /bin/sh

if [ "$#" -lt 1 ]
then
    echo "Usage: $0 [Bluemix-Container-Registry-Namespace]"
    exit -1
fi


NAMESPACE=$1

docker build -t flask-base ./containers/flask-base/
docker tag flask-base $NAMESPACE/flask-base
docker push $NAMESPACE/flask-base

docker build -t trevor-flask ./containers/trevor-flask/
docker tag trevor-flask $NAMESPACE/trevor-flask
docker push $NAMESPACE/trevor-flask

docker build -t nginx ./containers/trevor-nginx/
docker tag nginx $NAMESPACE/trevor-nginx
docker push $NAMESPACE/trevor-nginx
