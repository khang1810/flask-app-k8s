# Flask Application for Kubernetes

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Compatible-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

A production-ready Flask application designed specifically for Kubernetes deployment with health checks, logging, and proper configuration management.

## Features

- ✅ **Production-ready Flask application**
- ✅ **Kubernetes-native** with liveness and readiness probes
- ✅ **Comprehensive health checks** (`/health`, `/ready`, `/info`)
- ✅ **Structured logging** with proper log levels
- ✅ **Environment-based configuration** via environment variables
- ✅ **Security best practices** (non-root user, read-only filesystem)
- ✅ **Resource limits and requests** for Kubernetes
- ✅ **Complete test suite** with unit and integration tests
- ✅ **Docker optimized** with multi-stage considerations
- ✅ **ConfigMap support** for external configuration

## Project Structure

```
flask-app-k8s/
├── app.py                 # Main Flask application
├── Dockerfile             # Production-ready Docker image
├── deployment.yaml        # Kubernetes deployment with best practices
├── kubeconfig.yaml        # Local Kubernetes cluster configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── test_app.py            # Comprehensive test suite
├── README.md              # This documentation
└── .venv/                 # Python virtual environment (optional)
```

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster (Minikube, Kind, Docker Desktop, or cloud provider)
- kubectl

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-app-k8s
   ```

2. **Setup virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

5. **Run tests**
   ```bash
   python -m pytest test_app.py -v
   # or
   python test_app.py
   ```

### Environment Variables

The application supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host to bind the application |
| `PORT` | `5000` | Port to listen on |
| `APP_NAME` | `Flask-K8s-App` | Application name for display |
| `ENVIRONMENT` | `development` | Environment context |

### Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Main application endpoint | "Hello from {APP_NAME} on Kubernetes!" |
| `/health` | GET | Liveness probe for Kubernetes | JSON with status: healthy |
| `/ready` | GET | Readiness probe for Kubernetes | JSON with status: ready |
| `/info` | GET | Application information | JSON with app details |

## Docker Usage

### Build the Docker image
```bash
docker build -t flask-k8s:latest .
```

### Run locally with Docker
```bash
docker run -p 5000:5000 flask-k8s:latest
```

### Test Docker container
```bash
# Health check
curl http://localhost:5000/health

# Main endpoint
curl http://localhost:5000/
```

## Kubernetes Deployment

### Apply the deployment
```bash
kubectl apply -f deployment.yaml
```

### Check deployment status
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

### Access the application
```bash
# For LoadBalancer service
kubectl get service flask-service

# For local clusters (Minikube)
minikube service flask-service

# Port forwarding (alternative)
kubectl port-forward service/flask-service 8080:80
# Then access http://localhost:8080
```

### View logs
```bash
kubectl logs -l app=flask
```

## Kubernetes Configuration Details

### Resource Management
- **CPU Request**: 100m (0.1 CPU)
- **CPU Limit**: 200m (0.2 CPU)
- **Memory Request**: 64Mi
- **Memory Limit**: 128Mi

### Health Probes
- **Liveness Probe**: Checks `/health` every 10s after 5s initial delay
- **Readiness Probe**: Checks `/ready` every 5s after 2s initial delay

### Security Context
- Runs as non-root user (UID 1000)
- Read-only root filesystem
- Privilege escalation disabled
- All capabilities dropped

## Testing

The application includes a comprehensive test suite:

```bash
# Run all tests
python test_app.py

# Run specific test
python -m unittest test_app.FlaskAppTestCase.test_home_endpoint
```

Tests cover:
- Home endpoint functionality
- Health and readiness endpoints
- Info endpoint with environment variables
- Error handling for non-existent routes

## Production Considerations

### Security
- Always use TLS in production (add ingress controller with SSL)
- Update the `kubeconfig.yaml` to use proper certificates
- Remove `insecure-skip-tls-verify: true` for production clusters

### Scaling
- Adjust `replicas` in `deployment.yaml` based on load
- Consider Horizontal Pod Autoscaler (HPA) for automatic scaling

### Monitoring
- Integrate with Prometheus for metrics collection
- Use structured logging for centralized log aggregation
- Set up alerts based on health check failures

### Configuration Management
- Use ConfigMaps and Secrets for external configuration
- Avoid hardcoding sensitive information in deployment files

## Troubleshooting

### Common Issues

**1. Docker build fails**
- Ensure `requirements.txt` exists and is properly formatted
- Check internet connectivity for package downloads

**2. Kubernetes pods crash**
- Check pod logs: `kubectl logs <pod-name>`
- Verify image exists locally: `docker images | grep flask-k8s`
- Ensure sufficient resources are available in the cluster

**3. Health checks failing**
- Verify the application starts within the initial delay period
- Check that the correct ports are exposed and mapped

**4. Service not accessible**
- Verify service type matches your cluster capabilities
- For local development, LoadBalancer may require Minikube tunnel

### Debugging Commands

```bash
# Check pod status and events
kubectl describe pod -l app=flask

# Check service configuration
kubectl describe service flask-service

# Exec into container for debugging
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods -l app=flask
```

---

## Useful Commands Reference

### Local Development Commands

```bash
# Setup virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
python app.py

# Run with custom configuration
HOST=127.0.0.1 PORT=8080 APP_NAME="My-App" python app.py

# Run tests
python test_app.py
python -m unittest test_app.py -v
python -m pytest test_app.py -v --cov=app

# Check Python version
python --version

# List installed packages
pip list
pip freeze
```

### Docker Commands

```bash
# Build Docker image
docker build -t flask-k8s:latest .

# Build with no cache (fresh build)
docker build --no-cache -t flask-k8s:latest .

# List Docker images
docker images
docker images | grep flask

# Run container in foreground
docker run -p 5000:5000 flask-k8s:latest

# Run container in background (detached)
docker run -d -p 5000:5000 --name flask-app flask-k8s:latest

# Run with custom environment variables
docker run -d -p 5000:5000 -e APP_NAME="My-App" -e ENVIRONMENT=production flask-k8s:latest

# View container logs
docker logs flask-app
docker logs -f flask-app          # Follow logs
docker logs --tail 100 flask-app  # Last 100 lines

# List running containers
docker ps
docker ps -a                       # All containers including stopped

# Execute command inside container
docker exec -it flask-app /bin/sh
docker exec -it flask-app python --version

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/ready
curl http://localhost:5000/info

# Stop and remove container
docker stop flask-app
docker rm flask-app

# Remove image
docker rmi flask-k8s:latest

# Clean up all stopped containers and unused images
docker system prune -a

# Inspect image details
docker inspect flask-k8s:latest

# Check image size
docker images flask-k8s --format "{{.Repository}}:{{.Tag}} - {{.Size}}"
```

### Kubernetes Commands

```bash
# Apply configuration
kubectl apply -f deployment.yaml
kubectl apply -f .                 # Apply all YAML files in directory

# Get resources
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get configmaps
kubectl get all

# Get with labels
kubectl get pods --show-labels
kubectl get pods -l app=flask

# Watch resources in real-time
kubectl get pods -w
kubectl get deployments -w

# Describe resources (detailed info)
kubectl describe deployment flask-app
kubectl describe pod <pod-name>
kubectl describe service flask-service

# View logs
kubectl logs -l app=flask
kubectl logs -l app=flask -f       # Follow logs
kubectl logs -l app=flask --tail=100
kubectl logs <pod-name>            # Specific pod
kubectl logs -l app=flask -c flask-container  # Specific container

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -- python --version
kubectl exec -it <pod-name> -- env  # View environment variables

# Port forwarding
kubectl port-forward service/flask-service 8080:80
kubectl port-forward <pod-name> 5000:5000

# Access via browser (Minikube)
minikube service flask-service
minikube service flask-service --url

# Scale deployment
kubectl scale deployment flask-app --replicas=3
kubectl scale deployment flask-app --replicas=1

# Restart deployment (rolling restart)
kubectl rollout restart deployment flask-app

# Check rollout status
kubectl rollout status deployment flask-app
kubectl rollout history deployment flask-app

# Delete resources
kubectl delete -f deployment.yaml
kubectl delete deployment flask-app
kubectl delete service flask-service
kubectl delete pod <pod-name>      # Pod will be recreated by deployment
kubectl delete pods -l app=flask   # Delete all pods with label

# View resource usage
kubectl top pods -l app=flask
kubectl top nodes

# Check events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -w              # Watch events in real-time

# Validate YAML syntax (dry-run)
kubectl apply -f deployment.yaml --dry-run=client
kubectl apply -f deployment.yaml --dry-run=server

# Export configuration
kubectl get deployment flask-app -o yaml > export-deployment.yaml
kubectl get service flask-service -o yaml > export-service.yaml

# Edit live configuration
kubectl edit deployment flask-app
kubectl edit service flask-service

# Context management
kubectl config get-contexts
kubectl config use-context <context-name>
kubectl config current-context

# Cluster info
kubectl cluster-info
kubectl version --client
kubectl version --short
```

### Testing Endpoints

```bash
# Using curl
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/ready
curl http://localhost:5000/info

# Using curl with pretty JSON output
curl -s http://localhost:5000/health | python -m json.tool
curl -s http://localhost:5000/info | python -m json.tool

# Using wget
wget -qO- http://localhost:5000/

# Test from inside Kubernetes cluster
kubectl run test-curl --image=curlimages/curl --rm -it --restart=Never -- http://flask-service/health

# Load testing (requires hey or ab)
hey -n 1000 -c 10 http://localhost:5000/
ab -n 1000 -c 10 http://localhost:5000/
```

### Git Commands (for version control)

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Check status
git status
git diff

# Create branch
git checkout -b feature/new-feature

# Merge branch
git checkout main
git merge feature/new-feature

# Push to remote
git remote add origin <repository-url>
git push -u origin main
```

### Quick Reference Table

| Task | Command |
|------|---------|
| Start app locally | `python app.py` |
| Run tests | `python test_app.py` |
| Build Docker image | `docker build -t flask-k8s:latest .` |
| Run Docker container | `docker run -p 5000:5000 flask-k8s:latest` |
| Deploy to K8s | `kubectl apply -f deployment.yaml` |
| Check pods | `kubectl get pods -l app=flask` |
| View logs | `kubectl logs -l app=flask -f` |
| Scale to 5 replicas | `kubectl scale deployment flask-app --replicas=5` |
| Port forward | `kubectl port-forward service/flask-service 8080:80` |
| Delete deployment | `kubectl delete -f deployment.yaml` |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation and community
- Kubernetes best practices guides
- Docker security recommendations