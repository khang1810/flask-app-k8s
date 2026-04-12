# Flask Application for Kubernetes - Project Context

## Project Overview

This is a **production-ready Flask web application** designed specifically for Kubernetes deployment. The application serves a simple "Hello from Flask on Kubernetes!" message and includes comprehensive health checks, structured logging, and proper configuration management.

**Key Technologies:**
- **Backend Framework**: Flask 2.3.3 (Python 3.9)
- **Containerization**: Docker (python:3.9-slim base image)
- **Orchestration**: Kubernetes (Deployment, Service, ConfigMap)
- **Testing**: Python unittest framework

**Architecture:**
- Single Flask application with 4 endpoints (/, /health, /ready, /info)
- Containerized using Docker with security best practices (non-root user, read-only filesystem)
- Deployed to Kubernetes with 2 replicas, liveness/readiness probes, and resource limits
- Uses local Docker image (`flask-k8s:latest`) with `imagePullPolicy: Never`

## File Structure

```
flask-app-k8s/
├── app.py                    # Main Flask application with health checks
├── Dockerfile                # Production-ready Docker image
├── deployment.yaml           # Kubernetes deployment, service, and configmap
├── kubeconfig.yaml           # Local Kubernetes cluster configuration
├── requirements.txt          # Production dependencies (Flask==2.3.3)
├── requirements-dev.txt      # Development dependencies
├── test_app.py               # Comprehensive test suite
├── README.md                 # User-facing documentation
├── QWEN.md                   # This instructional context file
└── .venv/                    # Python virtual environment
```

## Building and Running

### Local Development

1. **Setup Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

2. **Activate Virtual Environment**:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application Locally**:
   ```bash
   python app.py
   ```
   The app will be available at `http://localhost:5000`

5. **Run Tests**:
   ```bash
   python test_app.py
   ```

### Docker Build and Run

1. **Build Docker Image**:
   ```bash
   docker build -t flask-k8s:latest .
   ```

2. **Run Container**:
   ```bash
   docker run -p 5000:5000 flask-k8s:latest
   ```

3. **Test Endpoints**:
   ```bash
   curl http://localhost:5000/
   curl http://localhost:5000/health
   curl http://localhost:5000/ready
   ```

### Kubernetes Deployment

1. **Apply Configuration**:
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Verify Deployment**:
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

3. **Access the Service**:
   - For LoadBalancer: `kubectl get service flask-service`
   - For Minikube: `minikube service flask-service`
   - Port forwarding: `kubectl port-forward service/flask-service 8080:80`

4. **View Logs**:
   ```bash
   kubectl logs -l app=flask
   ```

## Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Main application | "Hello from {APP_NAME} on Kubernetes!" |
| `/health` | GET | Liveness probe | JSON: `{status: "healthy", service, version}` |
| `/ready` | GET | Readiness probe | JSON: `{status: "ready", service, ready: true}` |
| `/info` | GET | Application info | JSON: `{app_name, host, port, environment}` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Host to bind the application |
| `PORT` | `5000` | Port to listen on |
| `APP_NAME` | `Flask-K8s-App` | Application name for display |
| `ENVIRONMENT` | `development` | Environment context |

## Development Conventions

### Code Style
- Simple, minimal Flask application structure
- Uses structured logging with proper log levels
- Follows Flask conventions for route definitions
- Environment-based configuration via `os.getenv()`

### Testing Practices
- Unit tests using Python's built-in `unittest` framework
- Tests cover all endpoints (home, health, ready, info)
- Tests verify HTTP status codes and response content
- Run tests with: `python test_app.py`

### Docker Best Practices
- Uses slim base image for smaller footprint
- Installs dependencies with `--no-cache-dir`
- Creates non-root user for security
- Includes HEALTHCHECK instruction
- Uses multi-layer caching strategy (requirements copied first)

### Kubernetes Best Practices
- **Resource Management**: CPU/memory requests and limits defined
- **Health Probes**: Liveness and readiness probes configured
- **Security Context**: Non-root, read-only filesystem, no privilege escalation
- **Labels**: Consistent labeling for app and version
- **ConfigMap**: External configuration support

## Kubernetes Configuration Details

### Deployment
- **Name**: `flask-app`
- **Replicas**: 2
- **Container**: `flask-container`
- **Image**: `flask-k8s:latest`
- **Port**: 5000

### Resource Limits
- **CPU Request**: 100m | **Limit**: 200m
- **Memory Request**: 64Mi | **Limit**: 128Mi

### Health Probes
- **Liveness**: HTTP GET `/health`, initial delay 5s, period 10s
- **Readiness**: HTTP GET `/ready`, initial delay 2s, period 5s

### Service
- **Name**: `flask-service`
- **Type**: LoadBalancer
- **Port**: 80 → 5000

## Common Commands

```bash
# Local development
python app.py
python test_app.py

# Docker
docker build -t flask-k8s:latest .
docker run -p 5000:5000 flask-k8s:latest
docker images | grep flask-k8s

# Kubernetes
kubectl apply -f deployment.yaml
kubectl get pods -l app=flask
kubectl logs -l app=flask
kubectl describe pod -l app=flask
kubectl delete -f deployment.yaml
```

## Troubleshooting

### Common Issues

1. **Docker build fails**: Ensure `requirements.txt` exists and is properly formatted
2. **Kubernetes pods crash**: Check logs with `kubectl logs -l app=flask`
3. **Health checks failing**: Verify application starts within initial delay period
4. **Service not accessible**: For local clusters, use `minikube service` or port-forwarding

### Debugging Commands
```bash
kubectl describe pod -l app=flask
kubectl describe service flask-service
kubectl exec -it <pod-name> -- /bin/sh
```

## Project Status

✅ **Complete and Production-Ready**

- All endpoints implemented and tested
- Docker image builds successfully
- Kubernetes deployment validated
- Comprehensive documentation provided
- Security best practices implemented
- Resource limits configured
- Health checks working
