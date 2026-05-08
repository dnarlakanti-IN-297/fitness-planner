# CloudBees Unify + ArgoCD Integration Guide

Complete guide for the GitOps CI/CD pipeline integrating **CloudBees Unify** (CI) with **ArgoCD** (CD) for the Fitness Planner application.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline Flow                          │
└──────────────────────────────────────────────────────────────────────┘

  Developer
     │
     │ git push
     ▼
  GitHub (main branch)
     │
     │ webhook
     ▼
  ┌─────────────────────────────────────┐
  │   CloudBees Unify (CI Pipeline)     │
  ├─────────────────────────────────────┤
  │ 1. test:    Run pytest with Smart   │
  │             Tests (subset testing)  │
  │                                     │
  │ 2. build:   Build Docker image      │
  │             Tag: commit-SHA         │
  │             Push to Docker Hub      │
  │                                     │
  │ 3. deploy:  Update k8s manifest     │
  │             Update image tag        │
  │             Commit & push to Git    │
  └─────────────────────────────────────┘
     │
     │ git push (updated manifest)
     ▼
  GitHub (k8s/deployment.yaml updated)
     │
     │ poll (every 3 min)
     ▼
  ┌─────────────────────────────────────┐
  │         ArgoCD (CD Tool)            │
  ├─────────────────────────────────────┤
  │ 1. Detects manifest change in Git   │
  │ 2. Compares with cluster state      │
  │ 3. Syncs (applies changes)          │
  │ 4. Monitors health                  │
  └─────────────────────────────────────┘
     │
     │ kubectl apply
     ▼
  ┌─────────────────────────────────────┐
  │    Kubernetes Cluster (Minikube)    │
  ├─────────────────────────────────────┤
  │ • Deployment: fitness-planner       │
  │ • Replicas: 2 pods                  │
  │ • Service: LoadBalancer (port 80)   │
  │ • Namespace: fitness-planner        │
  └─────────────────────────────────────┘
     │
     ▼
  Running Application! 🚀
```

## Key Concepts

### GitOps
**Git is the single source of truth**. All infrastructure and application configs live in Git. Changes go through Git, not `kubectl` commands.

### Separation of Concerns
- **CloudBees Unify** = CI (Continuous Integration)
  - Build, test, publish artifacts
- **ArgoCD** = CD (Continuous Deployment)
  - Deploy, sync, monitor Kubernetes resources

### Benefits
✅ **Audit Trail** - Every deployment is a Git commit  
✅ **Easy Rollback** - Just `git revert` or rollback in ArgoCD UI  
✅ **Declarative** - Desired state in Git, ArgoCD ensures cluster matches  
✅ **Self-Healing** - If someone manually changes cluster, ArgoCD reverts it  
✅ **No Cluster Access Needed** - Developers never need kubectl/cluster credentials  

---

## Prerequisites Setup

### 1. Local Kubernetes (Minikube)

```bash
# Install Minikube
brew install minikube

# Install QEMU driver (for Apple Silicon Macs)
brew install qemu

# Start Minikube
minikube start --memory=4096 --cpus=2 --driver=qemu

# Verify
kubectl cluster-info
kubectl get nodes
```

### 2. Install ArgoCD

```bash
cd ~/fitness-planner

# Run installation script
./argocd/install-argocd.sh

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open: https://localhost:8080
# Username: admin
# Password: (from command above)
```

### 3. Deploy Application to ArgoCD

```bash
# Apply ArgoCD application manifest
kubectl apply -f argocd/application.yaml

# Verify
kubectl get application -n argocd
kubectl get pods -n fitness-planner
```

---

## Workflow Files

### Main CI Workflow (`.cloudbees/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Manual trigger via `workflow_dispatch`

**Jobs:**

#### 1. **test** - Run tests with Smart Tests
- Checkout code with full Git history
- Verify Smart Tests connectivity
- Record build and session context
- Collect all tests with pytest
- Generate Smart Tests subset (50% target)
- Run only the subset of tests
- Record test results
- Publish test results and evidence

**Smart Tests Benefits:**
- Runs only tests affected by code changes
- Saves 50%+ of test execution time
- Learns from test history
- Still provides full coverage over time

#### 2. **build** - Build and push Docker image
- Calls reusable workflow: `build-reusable.yml`
- Builds image with Kaniko (no Docker daemon needed)
- Tags image with commit SHA: `dnarlakanti/fitness-planner:<commit-sha>`
- Pushes to Docker Hub
- Publishes build evidence

#### 3. **deploy** - Update Kubernetes manifest
- Calls workflow: `update-manifest.yml`
- Updates `k8s/deployment.yaml` with new image tag
- Commits change with message: "Deploy image <SHA> via Unify CI [skip ci]"
- Pushes to GitHub
- ArgoCD detects change and deploys automatically

**Note:** `[skip ci]` in commit message prevents infinite loop (Unify doesn't trigger again on its own commit)

---

### Update Manifest Workflow (`.cloudbees/workflows/update-manifest.yml`)

**Purpose:** Updates Kubernetes manifest after successful build

**Inputs:**
- `image-tag` (required) - Docker image tag (typically commit SHA)

**Steps:**
1. Checkout code
2. Update `k8s/deployment.yaml` image field using `sed`
3. Commit and push to GitHub (if changes detected)

**Example Result:**
```yaml
# Before
image: nginx:alpine

# After
image: dnarlakanti/fitness-planner:abc123def456
```

---

## ArgoCD Application Configuration

### Main Application (`argocd/application.yaml`)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fitness-planner
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/dnarlakanti-IN-297/fitness-planner.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: fitness-planner
  syncPolicy:
    automated:
      prune: true        # Delete resources removed from Git
      selfHeal: true     # Revert manual cluster changes
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

**Key Settings:**
- `automated.prune: true` - Removes resources deleted from Git
- `automated.selfHeal: true` - Reverts manual kubectl changes
- `syncOptions.CreateNamespace` - Auto-creates namespace if missing

---

## Complete CI/CD Flow Example

### Scenario: Fixing a bug in the fitness planner

```bash
# 1. Developer makes code change
cd ~/fitness-planner
vim app/calculators.py  # Fix BMI calculation bug
git add app/calculators.py
git commit -m "Fix BMI calculation for edge case"
git push origin main
```

**What happens next (automatically):**

#### Phase 1: CloudBees Unify CI (3-5 minutes)

```
✅ Unify detects push to main branch
✅ Job: test
   ├─ Checkout code
   ├─ Smart Tests records build context
   ├─ Collects all 15 tests
   ├─ Generates subset: 7 tests (affected by change)
   ├─ Runs 7 tests (saves 53% time!)
   └─ All tests pass ✅

✅ Job: build
   ├─ Checkout code
   ├─ Kaniko builds Docker image
   ├─ Tags: dnarlakanti/fitness-planner:abc123def456
   ├─ Pushes to Docker Hub
   └─ Image ready ✅

✅ Job: deploy
   ├─ Checkout code
   ├─ Updates k8s/deployment.yaml
   │  Old: image: nginx:alpine
   │  New: image: dnarlakanti/fitness-planner:abc123def456
   ├─ Commits: "Deploy image abc123def456 via Unify CI [skip ci]"
   └─ Pushes to GitHub ✅
```

#### Phase 2: ArgoCD CD (1-3 minutes)

```
✅ ArgoCD polls GitHub (every 3 min)
✅ Detects change in k8s/deployment.yaml
✅ Compares Git (desired) vs Cluster (current)
   ├─ Git:     dnarlakanti/fitness-planner:abc123def456
   ├─ Cluster: nginx:alpine
   └─ Status: OutOfSync

✅ ArgoCD syncs (applies changes)
   ├─ Creates new ReplicaSet
   ├─ Starts new pods with image abc123def456
   ├─ Waits for pods to be Ready
   ├─ Terminates old pods
   └─ Status: Synced, Healthy ✅

✅ Application updated! 🚀
```

---

## Monitoring & Operations

### ArgoCD UI

```bash
# Port-forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Open browser
open https://localhost:8080

# Login
# Username: admin
# Password: (get with command below)
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**In the UI you can:**
- View sync status (Synced/OutOfSync)
- See deployment history
- View resource tree (pods, services, etc.)
- Manually sync
- Rollback to previous version
- View diff between Git and cluster

### ArgoCD CLI

```bash
# Install CLI
brew install argocd

# Login
argocd login localhost:8080

# View application
argocd app get fitness-planner

# Sync manually (force immediate deployment)
argocd app sync fitness-planner

# View history
argocd app history fitness-planner

# Rollback
argocd app rollback fitness-planner <REVISION>

# View logs
argocd app logs fitness-planner
```

### kubectl Commands

```bash
# Check application status
kubectl get application -n argocd

# Check pods
kubectl get pods -n fitness-planner

# View pod logs
kubectl logs -n fitness-planner -l app=fitness-planner -f

# Describe pod (for troubleshooting)
kubectl describe pod -n fitness-planner <POD_NAME>

# Check service
kubectl get svc -n fitness-planner

# Access application
minikube service fitness-planner -n fitness-planner
```

---

## Troubleshooting

### Issue: ArgoCD shows "OutOfSync" but won't sync

**Solution:**
```bash
# Force refresh from Git
argocd app get fitness-planner --refresh

# Force sync
argocd app sync fitness-planner --force

# If still stuck, check application details
kubectl describe application fitness-planner -n argocd
```

### Issue: Pods crash after deployment

**Check logs:**
```bash
kubectl logs -n fitness-planner -l app=fitness-planner --tail=50
```

**Common causes:**
- Image architecture mismatch (x86 vs ARM)
- Missing environment variables
- Port configuration mismatch
- Health probe failures

**Solution for architecture mismatch:**
```bash
# Build multi-arch image
docker buildx build --platform linux/amd64,linux/arm64 \
  -t dnarlakanti/fitness-planner:TAG --push .
```

### Issue: Unify workflow fails at "deploy" job

**Check:**
1. GitHub token has write permissions
2. Commit message includes `[skip ci]`
3. Git user config is set correctly

**View Unify logs:**
- Go to CloudBees Unify UI
- Navigate to workflow run
- Check "deploy" job logs

### Issue: Image pull error

**Verify image exists:**
```bash
docker pull dnarlakanti/fitness-planner:TAG
```

**Check deployment:**
```bash
kubectl get deployment fitness-planner -n fitness-planner -o yaml | grep image:
```

---

## Testing the Integration

### Test 1: Manual Manifest Change

```bash
# Update replicas
sed -i '' 's/replicas: 2/replicas: 3/' k8s/deployment.yaml

# Commit and push
git add k8s/deployment.yaml
git commit -m "Scale to 3 replicas"
git push

# Wait for ArgoCD (max 3 min) or force sync
argocd app sync fitness-planner

# Verify
kubectl get pods -n fitness-planner
# Should show 3 pods
```

### Test 2: Full CI/CD Pipeline

```bash
# Make code change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "Test full pipeline"
git push

# Watch Unify workflow
# 1. Go to GitHub Actions or CloudBees Unify UI
# 2. Watch test → build → deploy jobs

# Watch ArgoCD deployment
argocd app get fitness-planner --watch

# Check pods
kubectl get pods -n fitness-planner -w
```

### Test 3: Rollback

```bash
# View deployment history in ArgoCD
argocd app history fitness-planner

# Rollback to previous version
argocd app rollback fitness-planner <REVISION_NUMBER>

# Verify rollback
kubectl get pods -n fitness-planner
argocd app get fitness-planner
```

---

## Multi-Environment Setup

For production use, you typically have multiple environments:

### Dev Environment

```yaml
# argocd/application-dev.yaml
spec:
  source:
    targetRevision: develop  # Tracks develop branch
  destination:
    namespace: fitness-planner-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true  # Auto-sync enabled for dev
```

Deploy:
```bash
kubectl apply -f argocd/application-dev.yaml
```

### Production Environment

```yaml
# argocd/application-prod.yaml
spec:
  source:
    targetRevision: main  # Tracks main branch
  destination:
    namespace: fitness-planner-prod
  syncPolicy:
    # No automated sync - manual approval required
    syncOptions:
      - CreateNamespace=true
```

Deploy:
```bash
kubectl apply -f argocd/application-prod.yaml

# Sync manually (requires approval)
argocd app sync fitness-planner-prod
```

**Best Practice:** Dev auto-syncs, Prod requires manual approval

---

## Security Best Practices

### 1. Use Image Digests

Instead of tags, use SHA256 digests for immutability:

```yaml
# Less secure (tag can be overwritten)
image: dnarlakanti/fitness-planner:v1.0.0

# More secure (digest is immutable)
image: dnarlakanti/fitness-planner@sha256:abc123...
```

Update Unify workflow to use digests:
```bash
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' dnarlakanti/fitness-planner:${TAG})
sed -i "s|image: .*|image: ${DIGEST}|" k8s/deployment.yaml
```

### 2. Separate Repos (Optional)

Many organizations use separate repos:
- `fitness-planner` - Application code
- `fitness-planner-gitops` - Kubernetes manifests only

**Benefits:**
- Different access controls
- Cleaner Git history
- Better separation of concerns

### 3. RBAC in ArgoCD

Restrict who can sync to production:

```yaml
# argocd-rbac-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.csv: |
    p, role:dev, applications, get, */*, allow
    p, role:dev, applications, sync, */fitness-planner-dev, allow
    p, role:ops, applications, *, */fitness-planner-prod, allow
```

---

## Cost Management (Minikube)

```bash
# Stop Minikube when not using
minikube stop

# Start again when needed
minikube start

# Delete cluster completely
minikube delete

# View resource usage
kubectl top nodes
kubectl top pods -n fitness-planner
```

---

## Next Steps for Production

1. **Use Kustomize** for environment-specific configs
   ```
   k8s/
   ├── base/
   │   ├── deployment.yaml
   │   └── service.yaml
   └── overlays/
       ├── dev/
       ├── staging/
       └── prod/
   ```

2. **Set up Notifications**
   - Slack alerts on deployment success/failure
   - Email notifications for prod deployments

3. **Implement Progressive Delivery**
   - Blue/Green deployments
   - Canary releases
   - Use ArgoCD Rollouts

4. **Add Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Distributed tracing

5. **Secrets Management**
   - Use Sealed Secrets or External Secrets Operator
   - Never commit plain secrets to Git

---

## Summary

**What You've Built:**
✅ GitOps CI/CD pipeline  
✅ CloudBees Unify handles CI (test, build)  
✅ ArgoCD handles CD (deploy, sync, monitor)  
✅ Git is single source of truth  
✅ Automatic deployment on code push  
✅ Easy rollback via Git or ArgoCD  
✅ Self-healing cluster state  

**Workflow:**
```
Code Push → Unify CI → Update Manifest → Push to Git → ArgoCD → Deploy to K8s
```

This is production-ready GitOps! 🚀

---

## Resources

- **ArgoCD Docs**: https://argo-cd.readthedocs.io
- **CloudBees Unify**: https://docs.cloudbees.com/
- **GitOps Principles**: https://www.gitops.tech/
- **Kubernetes Best Practices**: https://kubernetes.io/docs/concepts/configuration/overview/

---

## Support

For issues or questions:
1. Check ArgoCD logs: `kubectl logs -n argocd deployment/argocd-server`
2. Check application status: `kubectl describe application fitness-planner -n argocd`
3. View Unify workflow logs in CloudBees UI
4. Consult documentation links above
