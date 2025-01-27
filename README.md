# IoT Gateway Project with Istio and Kubernetes

## Overview

This project simulates an IoT system with multiple zones sending data to a central gateway, which then communicates with a backend server. The system is deployed on a Kubernetes cluster and uses Istio for traffic management, monitoring, and fault injection. The key use cases implemented include:

- **UC3bis**: Monitoring response time using Prometheus and alerting if thresholds are exceeded.
- **UC6**: Automatically blocking traffic from specific zones when errors or high traffic are detected.

## Architecture

The project consists of:

- **Zones**: Simulated IoT zones (Zone1, Zone2, Zone3) represented as pods.
- **IoT Gateway**: An intermediate gateway that processes requests from the zones.
- **IoT Server**: A backend server receiving data from the gateway.
- **Istio**: Service mesh used for traffic control and monitoring.

## Prerequisites

1. A Kubernetes cluster (e.g., Minikube, OpenShift, or a cluster on OpenStack).
2. `kubectl` installed and configured to interact with your cluster.
3. Istio installed on the cluster.
4. `istioctl` installed locally for managing Istio resources.
5. Prometheus, Grafana, and Kiali installed within the Istio system.
6. `curl` for testing endpoints.
7. Docker installed for building and pushing custom images.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-directory
```

### 2. Build Docker Images

Build and push the Docker images for zones, the gateway, and the server.

```bash
docker build -t <registry-url>/iot-zone-img:latest ./gf

docker build -t <registry-url>/iot-gateway-img:latest ./gi

docker build -t <registry-url>/iot-server-img:latest ./server
```

Push the images to your container registry:

```bash
docker push <registry-url>/iot-zone-img:latest
docker push <registry-url>/iot-gateway-img:latest
docker push <registry-url>/iot-server-img:latest
```

### 3. Deploy Kubernetes Resources

#### Deploy the IoT Zones

```bash
kubectl apply -f gf/zone1_deployment.yaml
kubectl apply -f gf/zone2_deployment.yaml
kubectl apply -f gf/zone3_deployment.yaml
kubectl apply -f gf/zone_cluster_ip.yaml
```

#### Deploy the IoT Gateway

```bash
kubectl apply -f gi/gateway_deployment.yaml
kubectl apply -f gi/gateway_cluster_ip.yaml
```

#### Deploy the IoT Server

```bash
kubectl apply -f server/server_deployment.yaml
kubectl apply -f server/server_cluster_ip.yaml
```

### 4. Configure Istio

#### Apply VirtualService and AuthorizationPolicy

To block traffic from specific zones when needed, apply the Istio configuration:

```bash
kubectl apply -f istio-config/virtualservice_block_z2_z3.yaml
kubectl apply -f istio-config/authorization_policy_deny_z2_z3.yaml
```

### 5. Run the Python Controller

The controller monitors the system and dynamically applies configuration based on Prometheus metrics.

```bash
python3 controller/gc.py
```

### 6. Test the System

You can simulate traffic using `curl` or load-testing tools like `hey`.

#### Send Requests from Zones

```bash
kubectl run curl-test --image=curlimages/curl -it --rm --restart=Never -n project -- /bin/sh
curl -H "app: iot-zone1" http://iot-gateway-clusterip.project.svc.cluster.local:8081
curl -H "app: iot-zone2" http://iot-gateway-clusterip.project.svc.cluster.local:8081
```

#### View Metrics and Logs

- **Kiali Dashboard**: Run `istioctl dashboard kiali` and navigate to the displayed URL.
- **Prometheus**: Run `istioctl dashboard prometheus`.
- **Grafana**: Run `istioctl dashboard grafana`.

### 7. Clean Up Resources

To remove the deployments and services:

```bash
kubectl delete namespace project
```

## Key Files

### Kubernetes Manifests

- `gf/zone1_deployment.yaml`: Deployment for Zone 1.
- `gi/gateway_deployment.yaml`: Deployment for the IoT Gateway.
- `server/server_deployment.yaml`: Deployment for the IoT Server.
- `istio-config/virtualservice_block_z2_z3.yaml`: Istio VirtualService to block traffic from Zone2 and Zone3.
- `istio-config/authorization_policy_deny_z2_z3.yaml`: Istio AuthorizationPolicy to block headers from Zone2 and Zone3.

### Controller Script

- `controller/gc.py`: Python script for monitoring and dynamically managing Istio configurations based on Prometheus metrics.

## Issues and Troubleshooting

1. **Pending Pods**:

   - Ensure nodes have enough memory and CPU.
   - Check `kubectl describe pod <pod-name>` for scheduling issues.

2. **Istio Configuration Errors**:

   - Ensure the VirtualService and AuthorizationPolicy configurations match your deployment.
   - Use `kubectl describe` to debug issues.

3. **Testing Failures**:

   - Verify service connectivity using `curl`.
   - Ensure proper headers (e.g., `app`) are sent with requests.
