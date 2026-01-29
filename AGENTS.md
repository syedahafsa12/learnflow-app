# AGENTS.md
Repository structure and guidelines for AI agents

## Root Files
- `AGENTS.md`
- `CLOUD_DEPLOYMENT_GUIDE.md`
- `hack.md`
- `.claude\settings.local.json`
- `.claude\skills\agents-md-gen\REFERENCE.md`
- `.claude\skills\agents-md-gen\SKILL.md`
- `.claude\skills\agents-md-gen\scripts\generate_agents_md.py`
- `.claude\skills\docusaurus-deploy\REFERENCE.md`
- `.claude\skills\docusaurus-deploy\SKILL.md`
- `.claude\skills\docusaurus-deploy\scripts\configure_site.sh`
- `.claude\skills\docusaurus-deploy\scripts\deploy.sh`
- `.claude\skills\docusaurus-deploy\scripts\verify_deployment.py`
- `.claude\skills\docusaurus-deploy\templates\docusaurus.config.js`
- `.claude\skills\fastapi-dapr-agent\REFERENCE.md`
- `.claude\skills\fastapi-dapr-agent\SKILL.md`
- `.claude\skills\fastapi-dapr-agent\scripts\add_dapr_config.sh`
- `.claude\skills\fastapi-dapr-agent\scripts\create_service.py`
- `.claude\skills\fastapi-dapr-agent\scripts\create_service.sh`
- `.claude\skills\fastapi-dapr-agent\scripts\deploy_service.sh`
- `.claude\skills\fastapi-dapr-agent\scripts\deploy_to_k8s.sh`
- `.claude\skills\fastapi-dapr-agent\scripts\verify_deployment.py`
- `.claude\skills\fastapi-dapr-agent\scripts\verify_service.py`
- `.claude\skills\k8s-foundation\REFERENCE.md`
- `.claude\skills\k8s-foundation\SKILL.md`
- `.claude\skills\k8s-foundation\scripts\check_cluster_health.py`
- `.claude\skills\k8s-foundation\scripts\setup_foundation.sh`
- `.claude\skills\k8s-foundation\scripts\verify_readiness.py`
- `.claude\skills\kafka-k8s-setup\REFERENCE.md`
- `.claude\skills\kafka-k8s-setup\SKILL.md`
- `.claude\skills\kafka-k8s-setup\scripts\create_topics.py`
- `.claude\skills\kafka-k8s-setup\scripts\create_topics.sh`
- `.claude\skills\kafka-k8s-setup\scripts\deploy.sh`
- `.claude\skills\kafka-k8s-setup\scripts\deploy_kafka.sh`
- `.claude\skills\kafka-k8s-setup\scripts\verify.py`
- `.claude\skills\kafka-k8s-setup\scripts\verify_kafka.py`
- `.claude\skills\mcp-code-execution\REFERENCE.md`
- `.claude\skills\mcp-code-execution\SKILL.md`
- `.claude\skills\mcp-code-execution\scripts\integration_demo.py`
- `.claude\skills\mcp-code-execution\scripts\mcp_client.py`
- `.claude\skills\mcp-code-execution\scripts\run_examples.sh`
- `.claude\skills\mcp-code-execution\scripts\examples\k8s_health_check.py`
- `.claude\skills\mcp-code-execution\scripts\examples\kafka_monitor.py`
- `.claude\skills\mcp-code-execution\scripts\examples\postgres_health_check.py`
- `.claude\skills\nextjs-k8s-deploy\REFERENCE.md`
- `.claude\skills\nextjs-k8s-deploy\SKILL.md`
- `.claude\skills\nextjs-k8s-deploy\scripts\build_deploy.sh`
- `.claude\skills\nextjs-k8s-deploy\scripts\configure_env.sh`
- `.claude\skills\nextjs-k8s-deploy\scripts\verify_deployment.py`
- `.claude\skills\nextjs-k8s-deploy\scripts\verify_nextjs.py`
- `.claude\skills\nextjs-k8s-deploy\templates\Dockerfile.nextjs`
- `.claude\skills\nextjs-k8s-deploy\templates\k8s\deployment.yaml`
- `.claude\skills\postgres-k8s-setup\REFERENCE.md`
- `.claude\skills\postgres-k8s-setup\SKILL.md`
- `.claude\skills\postgres-k8s-setup\scripts\deploy.sh`
- `.claude\skills\postgres-k8s-setup\scripts\deploy_postgres.sh`
- `.claude\skills\postgres-k8s-setup\scripts\run_migrations.py`
- `.claude\skills\postgres-k8s-setup\scripts\run_migrations.sh`
- `.claude\skills\postgres-k8s-setup\scripts\verify.py`
- `.claude\skills\postgres-k8s-setup\scripts\verify_postgres.py`
- `argocd\application.yaml`
- `argocd\kafka-application.yaml`
- `aws-deployment\eks-cluster.yaml`
- `aws-deployment\argocd\application.yaml`
- `aws-deployment\manifests\deployments.yaml`
- `aws-deployment\manifests\namespace.yaml`
- `aws-deployment\scripts\build-and-push-ecr.sh`
- `backend\schema.sql`
- `backend\code-review-agent\main.py`
- `backend\concepts-agent\main.py`
- `backend\debug-agent\main.py`
- `backend\exercise-agent\main.py`
- `backend\progress-agent\main.py`
- `backend\triage-agent\main.py`
- `cloud-deployment\azure\aks-deployment.yaml`
- `cloud-deployment\azure\deploy-to-azure.sh`
- `cloud-deployment\gcp\deploy-to-gcp.sh`
- `cloud-deployment\gcp\gke-deployment.yaml`
- `cloud-deployment\oracle\deploy-to-oracle.sh`
- `cloud-deployment\oracle\oke-deployment.yaml`
- `frontend\next.config.js`
- `frontend\pages\index.js`
- `frontend\pages\_app.js`
- `frontend\pages\api\tutor.js`
- `frontend\styles\globals.css`
- `frontend\styles\Home.module.css`
- `k8s\code-review-agent.yaml`
- `k8s\concepts-agent.yaml`
- `k8s\kafka-topics.yaml`
- `k8s\learnflow-namespace.yaml`
- `k8s\remaining-agents.yaml`
- `k8s\triage-agent.yaml`

## Configuration Files
- `README.md` - Important configuration file
- `argocd\README.md` - Important configuration file
- `aws-deployment\README.md` - Important configuration file
- `backend\code-review-agent\Dockerfile` - Important configuration file
- `backend\code-review-agent\requirements.txt` - Important configuration file
- `backend\concepts-agent\Dockerfile` - Important configuration file
- `backend\concepts-agent\requirements.txt` - Important configuration file
- `backend\debug-agent\Dockerfile` - Important configuration file
- `backend\debug-agent\requirements.txt` - Important configuration file
- `backend\exercise-agent\Dockerfile` - Important configuration file
- `backend\exercise-agent\requirements.txt` - Important configuration file
- `backend\progress-agent\Dockerfile` - Important configuration file
- `backend\progress-agent\requirements.txt` - Important configuration file
- `backend\triage-agent\Dockerfile` - Important configuration file
- `backend\triage-agent\requirements.txt` - Important configuration file
- `cloud-deployment\README.md` - Important configuration file
- `frontend\Dockerfile` - Important configuration file
- `frontend\package.json` - Important configuration file

## Directory Structure
## File Extensions and Technologies
Common file extensions and their purposes in this repository:
- `.py`: Python source code
- `.js`, `.jsx`: JavaScript/JSX code
- `.ts`, `.tsx`: TypeScript/TSX code
- `.md`: Documentation files
- `.yaml`, `.yml`: Configuration files
- `.json`: Data and configuration files
- `.sh`: Shell scripts
- `.sql`: Database scripts

## Guidelines for AI Agents
1. Respect the existing code style and patterns
2. Follow the established architecture and design principles
3. Maintain backward compatibility when possible
4. Update documentation when making changes
5. Consider the impact on related components
