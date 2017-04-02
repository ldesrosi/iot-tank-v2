#! /bin/sh

case "$1" in
  install)
      kubectl create -f local-volume.yaml
      kubectl create secret generic grafana-passwd --from-file=grafana-passwd.txt
      kubectl create -f influxdb-deployment.yaml
      kubectl create -f grafana-deployment.yaml
      ;;
  uninstall)
      kubectl delete -f local-volume.yaml
      kubectl delete secret generic grafana-passwd --from-file=grafana-passwd.txt
      kubectl delete -f influxdb-deployment.yaml
      kubectl delete -f grafana-deployment.yaml
      ;;

esac

exit 0
