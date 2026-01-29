---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes with migrations
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL
- Setting up persistent data storage
- Need database for application state

## Instructions
1. Run deployment: `bash scripts/deploy.sh`
2. Run migrations: `bash scripts/run_migrations.sh`
3. Verify status: `python scripts/verify.py`
4. Confirm database is accessible before proceeding.

## Validation
- [ ] PostgreSQL pod is Running
- [ ] Database is accessible
- [ ] Schema migrations applied

See [REFERENCE.md](./REFERENCE.md) for configuration options.
