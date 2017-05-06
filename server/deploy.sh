#! /bin/sh

if [ "$#" -lt 1 ]
then
    echo "Usage: $0 [install | uninstall]"
    exit -1
fi

cd deploy

case "$1" in
  install)
      kubectl create -f local-volume.yaml
      kubectl create secret generic grafana-passwd --from-file=grafana-passwd.txt
      kubectl create -f influxdb-deployment.yaml
      kubectl create -f grafana-deployment.yaml
      kubectl create -f trevor-flask-deployment.yaml
      kubectl create -f nginx-deployment.yaml
      ;;
  uninstall)
      kubectl delete -f local-volume.yaml
      kubectl delete secret grafana-passwd
      kubectl delete -f influxdb-deployment.yaml
      kubectl delete -f grafana-deployment.yaml
      kubectl delete -f trevor-flask-deployment.yaml
      kubectl delete -f nginx-deployment.yaml
      ;;

esac

exit 0
