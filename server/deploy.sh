#! /bin/sh

if [ "$#" -lt 1 ]
then
    echo "Usage: $0 [install | uninstall] [all|volume|grafana|influxdb|trevor|nginx]"
    exit -1
fi

cd deploy

command=""
if [ "$1" == "install"  ]
then
  command="create"
elif [ "$1" == "uninstall"  ]
then
  command="delete"
else
  echo "Usage: $0 [install | uninstall] [all|volume|grafana|influxdb|trevor|nginx]"
  exit -1
fi

if [ "$2" == "volume"  ] ;
then
    kubectl $command -f local-volume.yaml
fi

if [ "$2" == "all"  ] || [ "$2" == "grafana"  ] ;
then
  kubectl $command secret generic grafana-passwd --from-file=grafana-passwd.txt
  kubectl $command -f grafana-deployment.yaml
fi

if [ "$2" == "all"  ] || [ "$2" == "influxdb"  ] ;
then
  kubectl $command -f influxdb-deployment.yaml
fi

if [ "$2" == "all"  ] || [ "$2" == "trevor"  ] ;
then
  kubectl $command -f trevor-flask-deployment.yaml
fi

if [ "$2" == "all"  ] || [ "$2" == "nginx"  ] ;
then
  kubectl $command -f nginx-deployment.yaml
fi

if [ "$1" == "install"  ]
then
kubectl describe svc grafana influxdb trevor-flask nginx
fi

exit 0
