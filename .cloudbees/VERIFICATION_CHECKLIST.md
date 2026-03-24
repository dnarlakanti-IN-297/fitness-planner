# CloudBees Unify Verification Checklist

Use this checklist to verify and correct the template files against actual CloudBees Unify documentation.

## 📋 Pre-Flight Checks

### Access & Documentation
- [ ] I can access CloudBees Unify platform
- [ ] I have found the CloudBees Unify documentation
- [ ] I have read the "Getting Started" guide
- [ ] I have found example workflows/components

**Documentation URLs to check:**
- Main: https://docs.cloudbees.com/docs/cloudbees-unify/latest/
- Workflows: https://docs.cloudbees.com/docs/cloudbees-unify/latest/workflows/
- Kaniko: https://docs.cloudbees.com/docs/cloudbees-unify/latest/build-tools/kaniko

---

## 🗂️ Directory Structure

### Current Setup:
```
.cloudbees/
├── components/
│   └── test-and-publish.yml
└── workflows/
    ├── ci.yml
    └── build-reusable.yml
```

### Verify:
- [ ] Directory name is correct (`.cloudbees/` vs `.github/` vs something else)
- [ ] `components/` subdirectory is correct
- [ ] `workflows/` subdirectory is correct
- [ ] File naming conventions are correct

**What the docs say:**
```
TODO: Write down the correct structure from docs
```

---

## 🔧 Component Syntax (test-and-publish.yml)

### Fields to Verify:
- [ ] `name:` field name is correct
- [ ] `description:` field name is correct
- [ ] `inputs:` section syntax is correct
- [ ] `runs:` or `steps:` - which is correct?
- [ ] `using: composite` - is this correct?

### Actions References:
- [ ] How to reference setup-python action
- [ ] How to run shell commands
- [ ] How to publish test results

**What the docs say:**
```
TODO: Copy the correct component syntax from docs
```

**Example from docs:**
```yaml
TODO: Paste an example component from CloudBees docs
```

---

## 📦 Reusable Workflow Syntax (build-reusable.yml)

### Fields to Verify:
- [ ] `on: workflow_call` - is this correct?
- [ ] `inputs:` section syntax is correct
- [ ] `secrets:` section syntax is correct
- [ ] `permissions:` placement and syntax
- [ ] `jobs:` structure
- [ ] `runs-on:` runner specification

### Critical: Kaniko Action
- [ ] Found the Kaniko action reference in docs
- [ ] Correct action identifier: `__________________________`
- [ ] Required parameters identified
- [ ] Authentication method understood

**What the docs say about Kaniko:**
```
TODO: Copy the Kaniko action usage from docs
```

**Example from docs:**
```yaml
TODO: Paste the Kaniko action example from docs
```

---

## 🔄 Main Workflow Syntax (ci.yml)

### Fields to Verify:
- [ ] `on:` trigger syntax is correct
- [ ] `push:` trigger works
- [ ] Manual trigger works (workflow_dispatch or other?)
- [ ] `permissions:` syntax is correct
- [ ] `jobs:` structure
- [ ] Job dependencies (`needs:`)

### Critical: Calling Components & Reusable Workflows
- [ ] Found how to call a component in docs
- [ ] Correct syntax to call component: `__________________________`
- [ ] Found how to call reusable workflow in docs
- [ ] Correct syntax to call reusable workflow: `__________________________`
- [ ] Passing secrets to reusable workflows works

**What the docs say:**
```
TODO: Copy how to call components and reusable workflows
```

**Example from docs:**
```yaml
TODO: Paste examples of calling components and reusable workflows
```

---

## 🔐 Secrets & Authentication

### To Verify:
- [ ] Docker Hub secrets are set in CloudBees Unify
- [ ] Secret names match: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
- [ ] Secrets can be passed to reusable workflows
- [ ] Secrets syntax: `${{ secrets.NAME }}` or different?

**Where to set secrets in CloudBees Unify:**
```
TODO: Document how to set secrets in CloudBees Unify
```

---

## 🧪 Testing Plan

### Before Pushing to Repository:
1. [ ] Syntax validation (if CloudBees provides a validator)
2. [ ] Secrets are configured
3. [ ] Repository is connected to CloudBees Unify

### Initial Test:
1. [ ] Commit and push changes to a test branch
2. [ ] Manually trigger the workflow
3. [ ] Monitor test job execution
4. [ ] Check if test results are published
5. [ ] Monitor build job execution
6. [ ] Check if Docker image is pushed

### Expected Results:
- [ ] Test job runs successfully
- [ ] Test results are published
- [ ] Build job runs after test job
- [ ] Docker image is built with Kaniko
- [ ] Docker image is pushed to Docker Hub

---

## 📝 Corrections Needed

As you find issues, document them here:

### Issue 1:
- **File:** `____________________`
- **Line:** `____________________`
- **Problem:** `____________________`
- **Correct syntax:** `____________________`

### Issue 2:
- **File:** `____________________`
- **Line:** `____________________`
- **Problem:** `____________________`
- **Correct syntax:** `____________________`

### Issue 3:
- **File:** `____________________`
- **Line:** `____________________`
- **Problem:** `____________________`
- **Correct syntax:** `____________________`

---

## ✅ Final Verification

Once everything is working:

- [ ] All tests pass on CloudBees Unify
- [ ] Docker image is successfully built and pushed
- [ ] Workflow triggers correctly on push
- [ ] Workflow triggers correctly on manual dispatch
- [ ] Test results are published properly
- [ ] Documentation is updated with correct syntax

---

## 🎯 Next Steps After Verification

1. [ ] Update template files with correct syntax
2. [ ] Remove all `TODO` comments
3. [ ] Remove `⚠️ TEMPLATE` warnings
4. [ ] Test one more time to confirm
5. [ ] Consider removing `.github/` directory (GitHub Actions)
6. [ ] Update main README with CloudBees Unify instructions
7. [ ] Commit and celebrate! 🎉
