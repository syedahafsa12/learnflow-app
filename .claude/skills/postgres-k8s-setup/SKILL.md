---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes with initialization scripts and verification
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL on Kubernetes
- Setting up database for applications
- Need for persistent data storage
- Database for microservices architecture

## Instructions
1. Deploy PostgreSQL: `./scripts/deploy_postgres.sh`
2. Verify status: `python scripts/verify_postgres.py`
3. Run migrations if needed: `python scripts/run_migrations.py <migration_file>`
4. Confirm all pods are Running and database is accessible

## Prerequisites
- Kubernetes cluster (Minikube, Kind, or cloud provider)
- Helm 3.x installed
- kubectl configured to access cluster

## Expected Components
- PostgreSQL primary instance
- Persistent volume for data storage
- Service for database access
- Secret for database credentials

## Validation
- [ ] PostgreSQL pod in Running state
- [ ] Database service accessible
- [ ] Can connect to database successfully
- [ ] Persistent storage configured

See [REFERENCE.md](./REFERENCE.md) for advanced configuration options.