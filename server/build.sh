#! /bin/sh

if [ "$#" -lt 2 ]
then
    echo "Usage: $0 [Bluemix-Container-Registry-Namespace] [all|flask|nginx|trevor]"
    exit -1
fi


NAMESPACE=$1

if [ "$2" == "all"  ] || [ "$2" == "flask"  ] ;
then
docker build -t flask-base ./containers/flask-base/
docker tag flask-base $NAMESPACE/flask-base
docker push $NAMESPACE/flask-base
fi

if [ "$2" == "all"  ] || [ "$2" == "trevor"  ] ;
then
docker build -t trevor-flask ./containers/trevor-flask/
docker tag trevor-flask $NAMESPACE/trevor-flask
docker push $NAMESPACE/trevor-flask
fi

if [ "$2" == "all"  ] || [ "$2" == "nginx"  ] ;
then
docker build -t nginx ./containers/trevor-nginx/
docker tag nginx $NAMESPACE/trevor-nginx
docker push $NAMESPACE/trevor-nginx
fi
