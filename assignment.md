# Part 1 - Kubernetes Setup

## Set up a local K8s Cluster

Set up a 3-node cluster with 1 control-plane and 2 worker nodes.
Control-plane and worker nodes should be differentiated appropriately using node labels and taints.
You can use any Kubernetes distribution, such as:

- [kind](https://kind.sigs.k8s.io/) - Recommended for local development
- [minikube](https://minikube.sigs.k8s.io/) - Good for single-node testing
- [microk8s](https://microk8s.io/) - Lightweight production-grade
- [k3s](https://k3s.io/) - Minimal resource requirements

## Deploy the application to Kubernetes

Run the demo app in Kubernetes using resources of your choice. Pick the primitives that best fit a production-grade cluster and justify your selection in terms of security, scalability, reliability, and application life cycle management.

**Things to note about the app:**

- The application defines a ready route at `/readyz` and a health route at `/healthz`.
- The application is stateless, requires regular updates that are not disruptive to its availability, and, during a 24-hour window, experiences a non-uniform traffic distribution.
- The application is assumed to run in a multi-tenant cluster, where other applications from other teams might also be running. We want to isolate our application from traffic outside of its namespace.
- The application should run on worker nodes only (not on the control-plane).
- The application implements security best practices, such as running as non-root and with the minimal set of privileges required to perform its work.

Feel free to incorporate this knowledge in the design of your manifests and the overall cluster topology. There are plenty of ways to design this – what's important is to **clearly state assumptions and justifications to the design decisions**.

### Implementation Checklist

Implement and justify each of the following components:

**Core Infrastructure:**
- [ ] **Namespace & Isolation** – Deploy in dedicated namespace with meaningful labels and NetworkPolicy for traffic isolation
- [ ] **Node Placement** – Use nodeSelector/affinity to ensure pods run only on worker nodes
- [ ] **Workload Controller** – Choose appropriate controller (Deployment recommended for stateless apps) and justify selection
- [ ] **Service Exposure** – Create Service resource and justify exposure method (ClusterIP/NodePort/LoadBalancer)

**Application Configuration:**
- [ ] **Secrets Management** – Source `GREETING` from Kubernetes Secret (use stringData for simplicity)
- [ ] **Configuration Management** – Source `READINESS_DELAY_SEC` and `FAIL_RATE` from ConfigMap
- [ ] **Environment Variables** – Configure any additional deployment-specific variables as needed

**Operational Excellence:**
- [ ] **Health Probes** – Configure readiness and liveness probes (account for 10-second startup delay)
- [ ] **Resource Management** – Set CPU/memory requests and limits with clear justification (consider latency vs. cost trade-offs)
- [ ] **Security Configuration** – Implement SecurityContext with non-root user, read-only root filesystem, and minimal capabilities
- [ ] **Scaling Strategy** – Implement HorizontalPodAutoscaler using CPU/memory metrics (document metrics-server requirements)
- [ ] **Availability Protection** – Configure PodDisruptionBudget to ensure service availability during updates

**Advanced Considerations:**
- [ ] **Resource Quotas** – Consider namespace-level resource quotas for multi-tenancy
- [ ] **Monitoring Integration** – Ensure `/metrics` endpoint is accessible for monitoring setup

### Part 1 Acceptance Criteria

- [ ] Application accessible via port-forward to service on port 8000
- [ ] All health endpoints (`/healthz`, `/readyz`, `/work`, `/metrics`) respond correctly
- [ ] Resource requests/limits configured and justified in documentation
- [ ] Security context configured (non-root execution, minimal privileges)
- [ ] NetworkPolicy restricts traffic appropriately within namespace
- [ ] PodDisruptionBudget configured for high availability during updates
- [ ] SOLUTION.md explains **why** you chose specific primitives and overall design decisions
- [ ] Application successfully demonstrates configuration via Secret and ConfigMap

# Part 2 - GitOps

## Manage the application via ArgoCD

**Initial Setup:**
1. Deploy ArgoCD onto the cluster using standard installation manifests
2. Configure ArgoCD to connect to your chosen git repository
3. Create an ArgoCD Application resource that manages deployment to the `dev` namespace
4. Ensure the application is fully declarative - all resources deployed through ArgoCD (no manual kubectl apply)
5. Configure environment-specific settings for the `dev` environment

**Repository Options:**
- **Option A (Recommended)**: Use your assignment repository with local git server or push to a public/private remote repository
- **Option B (Alternative)**: Use a public repository like [guestbook](https://github.com/argoproj/argocd-example-apps/tree/master/helm-guestbook) to avoid git server setup complexity

**Repository Structure Recommendations:**
- Use Helm charts or Kustomize for environment-specific configurations
- Implement a structure that supports multiple environments without duplication
- Consider using ArgoCD's ApplicationSet for managing multiple environments

## Multi-Environment GitOps Setup

**Environment Management:**
1. Create a configuration structure that supports multiple environments without code duplication
2. Deploy a second instance of the application to the `prd` namespace with production-appropriate settings
3. Implement environment-specific configurations such as:
   - Different resource limits (prd should have higher limits)
   - Different replica counts (prd should have more replicas)
   - Environment-specific variables or configurations
4. Maintain DRY principles - avoid duplicating manifests

**Repository Flexibility:**
Whether using the provided Flask app or the guestbook example, the key is demonstrating effective multi-environment GitOps patterns and justifying your approach.

### Part 2 Acceptance Criteria

- [ ] ArgoCD successfully installed and accessible (provide UI screenshots)
- [ ] Applications deployed to both `dev` and `prd` namespaces via ArgoCD
- [ ] Environment-specific configurations clearly visible (different resource limits, replica counts, etc.)
- [ ] DRY principle maintained - no duplicated manifests between environments
- [ ] Configuration structure easily supports additional environments (demonstrate scalability)
- [ ] All applications show "Healthy" and "Synced" status in ArgoCD
- [ ] SOLUTION.md explains GitOps workflow, tooling choices, and multi-environment strategy
- [ ] Screenshots provided showing:
  - ArgoCD UI with both applications
  - Application details showing different configurations
  - Successful deployment status
- [ ] Documentation includes commands for accessing ArgoCD and managing applications
