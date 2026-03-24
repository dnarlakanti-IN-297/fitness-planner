# CloudBees Unify Syntax - What We Learned

Based on the official CloudBees example you provided, here's what we discovered:

## ✅ Confirmed Syntax

### 1. File Structure (Kubernetes-style!)
```yaml
apiVersion: automation.cloudbees.io/v1alpha1
kind: workflow  # or 'action' for components
name: workflow-name
```

**Key difference**: CloudBees uses Kubernetes-style YAML with `apiVersion` and `kind`

### 2. Triggers
```yaml
on:
  push:
    branches:
      - "*"
  workflow_dispatch:  # For manual triggers
```

**Status**: ✅ Same as GitHub Actions

### 3. Permissions
```yaml
permissions:
  scm-token-own: read
  scm-token-org: read
  id-token: read
```

**Key difference**: CloudBees-specific permission names

### 4. Jobs Structure
```yaml
jobs:
  build:
    steps:
      - name: Step name
        uses: action-name
```

**Status**: ✅ Similar to GitHub Actions (no `runs-on` needed)

### 5. Checkout Action
```yaml
- uses: cloudbees-io/checkout@v1
  with:
    repository: owner/repo-name  # Optional
```

**Key difference**: Use `cloudbees-io/checkout@v1` not `actions/checkout@v4`

### 6. Docker Hub Authentication
```yaml
- uses: cloudbees-io/configure-oci-credentials@v1
  with:
    registry: ${{ vars.DOCKER_REGISTRY }}  # or docker.io
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

**Key difference**: Use `configure-oci-credentials@v1` not `docker/login-action@v3`

### 7. Kaniko Build
```yaml
- uses: cloudbees-io/kaniko@v1
  kind: build  # ← Important!
  with:
    destination: registry/image:tag1,registry/image:tag2
    dockerfile: path/to/Dockerfile
    context: .
```

**Key difference**: Includes `kind: build` field

### 8. CloudBees Context Variables
```yaml
${{ cloudbees.version }}  # CloudBees version
${{ cloudbees.scm.sha }}  # Git commit SHA
${{ vars.VARIABLE_NAME }} # Variables (not secrets)
${{ secrets.SECRET_NAME }} # Secrets
```

**Key difference**: CloudBees-specific context like `cloudbees.version`

### 9. Running Shell Commands
```yaml
- uses: docker://alpine:latest
  shell: sh
  run: |
    echo "commands here"
```

**Status**: ✅ Can run shell commands in Docker containers

---

## ❓ Still Need to Verify

### 1. Reusable Workflows
**Question**: How do you call a reusable workflow in CloudBees?

**Current guess**:
```yaml
jobs:
  build:
    uses: ./.cloudbees/workflows/build-reusable.yml
```

**Where to find**: Search docs for "reusable workflow" or "call workflow"

### 2. Components/Actions
**Question**: How do you reference a custom component in a workflow?

**Current guess**:
```yaml
- uses: ./.cloudbees/components/test-and-publish
```

**Where to find**: Search docs for "custom action" or "component"

### 3. Python Setup Action
**Question**: What's the correct CloudBees action for setting up Python?

**Current guess**: `cloudbees-io/configure-python-version@v1`

**Where to find**: Search docs for "python" or "language setup"

### 4. Test Results Publishing
**Question**: What's the correct CloudBees action for publishing test results?

**Current guess**: `cloudbees-io/publish-test-results@v1`

**Where to find**: Search docs for "test results" or "junit"

### 5. Component Definition
**Question**: Do components use `kind: action` or something else?

**Current format**:
```yaml
apiVersion: automation.cloudbees.io/v1alpha1
kind: action
name: component-name
```

**Where to find**: Search docs for "create component" or "custom action"

### 6. Manual Trigger
**Question**: Is `workflow_dispatch` correct for manual triggers in CloudBees?

**Where to find**: Search docs for "manual trigger" or "workflow dispatch"

### 7. Job Dependencies
**Question**: Is `needs:` the correct way to make jobs run sequentially?

**Current format**:
```yaml
jobs:
  test:
    steps: ...
  build:
    needs: test  # ← Correct?
```

**Where to find**: Search docs for "job dependencies" or "sequential jobs"

---

## 📋 Updated Files Status

### ✅ Updated with Confirmed Syntax:
- `.cloudbees/workflows/build-reusable.yml`
  - Uses `apiVersion` and `kind`
  - Uses `cloudbees-io/checkout@v1`
  - Uses `cloudbees-io/configure-oci-credentials@v1`
  - Uses `cloudbees-io/kaniko@v1` with `kind: build`
  - Uses `${{ cloudbees.scm.sha }}`

### ⚠️ Needs Verification:
- `.cloudbees/workflows/ci.yml`
  - How to call reusable workflow?
  - Correct Python setup action?
  - Correct test results publishing action?

- `.cloudbees/components/test-and-publish.yml`
  - Is `kind: action` correct?
  - Can components use `using: composite`?
  - How to reference components in workflows?

---

## 🎯 Your Next Actions

### Immediate:
1. **Test the build workflow** first (it has the most confirmed syntax)
2. **Look for Python setup action** in CloudBees docs
3. **Look for test results publishing** in CloudBees docs

### Search Terms to Use:
- "cloudbees python"
- "cloudbees test results"
- "cloudbees reusable workflow"
- "cloudbees custom action"
- "cloudbees component"

### Where to Search:
- https://docs.cloudbees.com/docs/cloudbees-unify/latest/
- Search for "Actions" → Browse available actions
- Look for "Workflows" → Examples section

---

## 💡 Key Takeaways

1. **CloudBees ≠ GitHub Actions**
   - Different file format (Kubernetes-style)
   - Different action names (`cloudbees-io/*`)
   - Different context variables (`cloudbees.*`)

2. **Authentication is Different**
   - Use `configure-oci-credentials` not `docker/login-action`
   - Registry URL can be a variable

3. **Kaniko Needs `kind: build`**
   - This is unique to CloudBees
   - Don't forget this field!

4. **No Runner Specification**
   - CloudBees doesn't use `runs-on:`
   - Infrastructure is managed differently

---

## 🚀 What's Working vs What Needs Testing

| Feature | Status | Confidence |
|---------|--------|------------|
| File format (`apiVersion`/`kind`) | ✅ Confirmed | 100% |
| Checkout action | ✅ Confirmed | 100% |
| OCI credentials | ✅ Confirmed | 100% |
| Kaniko build | ✅ Confirmed | 100% |
| Push triggers | ✅ Confirmed | 100% |
| Permissions format | ✅ Confirmed | 100% |
| Python setup | ⚠️ Needs verification | 50% |
| Test publishing | ⚠️ Needs verification | 50% |
| Reusable workflows | ⚠️ Needs verification | 30% |
| Custom components | ⚠️ Needs verification | 30% |
| Manual trigger | ⚠️ Needs verification | 70% |
| Job dependencies | ⚠️ Needs verification | 80% |

Ready to test or need to find more examples?
