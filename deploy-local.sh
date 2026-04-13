#!/bin/bash

# deploy-local.sh - Deploy to local Docker Desktop Kubernetes

set -e

echo "Building Docker image..."
docker build -t flask-k8s:latest .

echo "Applying Kubernetes manifests..."
kubectl apply -f deployment.yaml

echo "Waiting for deployment rollout..."
kubectl rollout status deployment/flask-app --timeout=120s

echo "Deployment completed successfully!"
echo "Access the service at:"
if kubectl get service flask-service -o jsonpath='{.spec.type}' | grep -q LoadBalancer; then
    echo "  http://localhost (LoadBalancer)"
else
    echo "  Use 'kubectl port-forward service/flask-service 8080:80' then visit http://localhost:8080"
fi