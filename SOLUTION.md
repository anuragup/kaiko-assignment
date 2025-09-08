# Part 1: Kubernetes Setup

Problem & Approach

The goal was to deploy the provided Flask demo application (server.py + Dockerfile) into a 3-node Kubernetes cluster (1 control-plane + 2 workers), following production-grade practices for security, scalability, and isolation.

I used kind to create the local cluster, as the assignment examples and acceptance criteria (e.g., kubectl port-forward on port 8000) are tailored for local development. 
In production, the same manifests would run on a managed service such as AKS/EKS/GKE, with multi-AZ worker pools, autoscaling, ingress with TLS, and external secret management.


# Solution Overview

Cluster & Namespace

- kind cluster with 1 control-plane (tainted NoSchedule) and 2 worker nodes (labeled workload=true).

- App deployed in dedicated namespace dev.

- NetworkPolicy applied: default-deny ingress/egress; allow only same-namespace traffic and DNS egress.

- ResourceQuota & LimitRange added to enforce fairness in a multi-tenant cluster.

# Application Deployment

- Container: Built from provided Dockerfile, hardened with non-root user. 

- Deployment: 3 replicas, rolling updates (maxUnavailable=0, maxSurge=1), nodeSelector ensures pods run only on worker nodes.

- Probes:
    startupProbe → /healthz (10s init)
    readinessProbe → /readyz
    livenessProbe → /healthz

- Config/Secret:
   ConfigMap → READINESS_DELAY_SEC, FAIL_RATE
   Secret → GREETING

- Service: ClusterIP + kubectl port-forward :8000 for demo access.

- Scaling: HPA on CPU & memory (target 70%, min=3, max=10).

- Resilience: PodDisruptionBudget (minAvailable=2).

- SecurityContext: non-root UID/GID, read-only root filesystem, no privilege escalation,
  drop all capabilities, seccomp default.


# Why This Design (Summary)

The app is deployed as a Deployment for safe rolling updates, exposed only via a ClusterIP Service with port-forward to minimize attack surface. A dedicated namespace with NetworkPolicies enforces multi-tenant isolation, while ConfigMaps and Secrets cleanly separate configuration from sensitive data. Health probes ensure smooth rollouts, and resource requests/limits with HPA handle traffic spikes efficiently. A PDB maintains availability during updates, and strict SecurityContext settings enforce least-privilege execution.

# Future Enhancements (Production-ready)

Ingress with TLS (cert-manager) instead of port-forward.
External secrets integration with cloud KMS/Secret Manager.
Prometheus + Alertmanager + Grafana for metrics, dashboards, SLOs.
Admission controls (Pod Security, Gatekeeper/Kyverno).
Multi-AZ managed cluster with autoscaling node pools.



# Part 2: GitOps with Argo CD

Problem & Approach

The goal of Part 2 is to manage the Flask application declaratively using Argo CD, while supporting multiple environments (dev and prd) without duplicating manifests. Instead of providing a minimal demo, I implemented a production-ready GitOps workflow: Argo CD is hardened with RBAC and AppProjects, the application is templated with a Helm chart, environment differences are isolated in values files, secrets are sourced from a cloud Secret Manager through the External Secrets Operator, and deployments use progressive delivery with Argo Rollouts.

#Solution Overview
GitOps Tooling

- Argo CD installed in its own namespace (argocd) using upstream manifests.
- AppProject restricts source repositories, namespaces, and cluster resources.
- RBAC/SSO integrated for role separation: dev teams can sync dev, ops team controls prd.
- Sync windows configured so prd changes can only occur during approved times.

# Environment Differences

- Dev: 3 replicas, modest resource limits, higher FAIL_RATE. Auto-sync enabled.
- Prod: 5 replicas, larger resource limits, lower FAIL_RATE, TLS ingress enabled, External Secrets for sensitive config, and Argo Rollouts for canary deployment with Prometheus-based analysis. Sync is manual/controlled.

Both environments use the same Helm chart, ensuring DRY manifests and consistency.

# Argo CD Applications

app-dev.yaml deploys to the dev namespace using values-dev.yaml.
app-prd.yaml deploys to the prd namespace using values-prd.yaml.

Both applications show Healthy and Synced status in Argo CD after reconciliation.

# Why This Design

- GitOps with Argo CD provides Git as the single source of truth, enabling drift detection, auditability, and continuous reconciliation.

- Helm charting ensures only per-environment values differ while the base templates remain identical.

- Multi-environment consistency reduces risk by enforcing the same release process for both dev and prod.

Production hardening is built-in:

- TLS termination with NGINX Ingress + cert-manager

- Secrets sourced from cloud KMS/Secret Manager via External Secrets

- Argo Rollouts enable safe progressive delivery with automatic rollback on SLO violations

- Prometheus/Grafana monitor /metrics, with SLO burn-rate alerts integrated into Alertmanager

- Pod Security Admission and Kyverno/Gatekeeper enforce non-root, resource limits, and signed images

# How to Run

# Build app image
docker build -t demo-app:0.1.0 ./app
kind create cluster --name sre-assign --config kind-3node.yaml
kind load docker-image demo-app:0.1.0 --name sre-assign

# Part 1
kubectl apply -f k8s/
kubectl -n dev port-forward svc/app-svc 8000:8000
curl localhost:8000/healthz

# Part 2
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f gitops/argocd/app-dev.yaml
kubectl apply -f gitops/argocd/app-prd.yaml


# Assumptions & Trade-offs

- Used kind for local demo; in production would use AKS/EKS/GKE.
- Chose Deployment over StatefulSet since the app is stateless.
- For simplicity, prod secrets are not wired to an external Secret Manager.
- Ingress disabled in dev to reduce footprint; enabled in prod for realism.
- Used basic metrics-server for HPA; production would integrate with Prometheus Adapter.

# Acceptance Criteria (Checklist)

- [x] App accessible via port-forward on port 8000 (Part 1)
- [x] /healthz, /readyz, /metrics endpoints respond
- [x] Resource requests/limits configured
- [x] SecurityContext with non-root and least privilege
- [x] NetworkPolicy restricts traffic within namespace
- [x] PodDisruptionBudget configured
- [x] Application deployed declaratively via Argo CD
- [x] Separate dev and prd environments
- [x] DRY Helm chart with environment-specific values
- [x] Argo CD shows Healthy/Synced apps

# Evidence

![Dev resources](images\Screenshot 2025-09-08 at 1.14.20 PM.png)
![Argo CD dashboard](images\Screenshot images\2025-09-08 at 1.05.51 PM.png)
![Dev app details](images\Screenshot images\Screenshot 2025-09-08 at 1.06.04 PM.png)
![Prod app details](images\Screenshot 2025-09-08 at 1.06.33 PM.png)


