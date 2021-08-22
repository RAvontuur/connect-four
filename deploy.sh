kubectl apply -f kube-deploy.yaml

kubectl get deployments

kubectl get services

kubectl rollout status deployment/connect-four

curl http://localhost:30001/play/start
