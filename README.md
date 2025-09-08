# (Senior) Platform Engineer – GitOps Technical Assignment

As a platform engineer at Kaiko, you'll work with cutting-edge infrastructure technologies to support our AI/ML workloads for healthcare applications. This assignment evaluates your hands-on expertise in working with Kubernetes and implementing GitOps practices.

Please note that while the time needed to complete this technical assignment is flexible and can be adapted to your schedule, we expect it to be completed within a maximum of one standard work week. This ensures the assessment remains focused and relevant, while also giving you the flexibility to manage your time effectively.

## High Level Overview

- **Part 1 – Kubernetes Setup**:
  Deploy the Flask application on Kubernetes with production-grade configurations including health/readiness probes, resource management, security best practices, controlled rollouts, and blast-radius limitations. Choose appropriate Kubernetes resources and justify your decisions.

- **Part 2 – GitOps**:
  Set up a GitOps workflow using ArgoCD to manage application deployment and lifecycle across multiple environments.

## Application Details

**Primary Option**: Use the provided Flask application (`app/server.py`) which includes:
- **Port**: Runs on port 8000
- **Health Endpoints**: 
  - `/healthz` - Health check (always returns 200 OK)
  - `/readyz` - Readiness check (returns 503 for first 10 seconds, then 200)
  - `/work` - Main application endpoint with configurable failure rate
  - `/metrics` - Prometheus metrics endpoint
- **Configuration Requirements**: 
  - `GREETING` - Must be sourced from Kubernetes Secret
  - `READINESS_DELAY_SEC` - Configurable via ConfigMap (default: 10 seconds)
  - `FAIL_RATE` - Configurable via ConfigMap (default: 0.02)

**Alternative Option**: For Part 2 (GitOps), you may use a public repository like the [ArgoCD guestbook example](https://github.com/argoproj/argocd-example-apps/tree/master/helm-guestbook) to simplify git repository management. This is particularly useful if setting up a local git server or managing repository access is challenging.

## Starter Pack Structure

```
repo/
  app/
    server.py          # Flask application
    requirements.txt   # Python dependencies
    Dockerfile        # Container definition
  assignment.md       # Detailed technical requirements
  README.md          # This overview file
  SOLUTION.md        # ← Your implementation documentation
```

You may organize additional files (Kubernetes manifests, Helm charts, etc.) however you see fit.

## Environment Requirements

- **Kubernetes Cluster**: Local cluster recommended (kind, minikube, microk8s, k3s) or any available platform
- **Required Tools**: Docker + `kubectl`
- **Alternative**: If you cannot run a cluster locally, provide manifests/Helm charts with detailed behavior descriptions and assumptions

## Deliverables

Your git repository should contain:
1. **Kubernetes Resources**: YAML manifests, Helm charts, or Kustomize configurations for Part 1
2. **ArgoCD Configuration**: Application definitions and setup commands for Part 2  
3. **SOLUTION.md**: Comprehensive documentation covering:
   - How to set up and run the solution
   - Design decisions and justifications for both Kubernetes and GitOps choices
   - Trade-offs and assumptions made
   - Screenshots/evidence of successful deployment
   - If using guestbook alternative, explanation of approach and GitOps concepts demonstrated
4. **Updated README.md**: Clear instructions for running your implementation

**Submission Options**:
- **Zip file**: Alternative option containing all code, configurations, and documentation

**Note**: Ensure all components are properly documented regardless of chosen approach.

**Good luck! We're excited to see your approach to production infrastructure engineering.**
