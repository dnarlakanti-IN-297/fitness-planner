# CloudBees Unify Configuration

⚠️ **IMPORTANT: These are TEMPLATE files**

This directory contains CloudBees Unify workflow and component definitions.
The files here are based on common CI/CD patterns but **MUST be verified** against official CloudBees Unify documentation.

## Directory Structure

```
.cloudbees/
├── README.md                    # This file
├── components/                  # Reusable components/actions
│   └── test-and-publish.yml    # Test component
└── workflows/                   # Workflow definitions
    ├── ci.yml                  # Main CI workflow
    └── build-reusable.yml      # Reusable build workflow
```

## What You Need to Verify

Before using these files, check CloudBees Unify documentation for:

1. **Directory Location**
   - [ ] Is `.cloudbees/` the correct directory name?
   - [ ] Or should it be `.github/workflows/` (if CloudBees uses GitHub structure)?
   - [ ] Or a different location?

2. **File Names**
   - [ ] Correct naming conventions for workflows
   - [ ] Correct naming conventions for components

3. **Syntax**
   - [ ] YAML structure matches CloudBees Unify
   - [ ] Field names are correct
   - [ ] Action references use correct format

4. **Kaniko Action**
   - [ ] Correct way to reference Kaniko in CloudBees Unify
   - [ ] Required parameters
   - [ ] Authentication method for Docker Hub

5. **Triggers**
   - [ ] Correct syntax for push/manual triggers
   - [ ] Event names match CloudBees Unify

## Documentation Links

- Main docs: https://docs.cloudbees.com/docs/cloudbees-unify/latest/
- Workflows: https://docs.cloudbees.com/docs/cloudbees-unify/latest/workflows/
- Kaniko: https://docs.cloudbees.com/docs/cloudbees-unify/latest/build-tools/kaniko

## Current Status

- ✅ Directory structure created
- ⚠️ Template files created (need verification)
- ❌ Not tested on CloudBees Unify platform yet

## Next Steps

1. Access CloudBees Unify documentation
2. Verify syntax against actual examples
3. Update templates with correct CloudBees syntax
4. Test on CloudBees Unify platform
5. Once working, consider removing `.github/` (GitHub Actions) directory
