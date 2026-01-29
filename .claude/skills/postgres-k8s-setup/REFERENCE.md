# PostgreSQL Kubernetes Setup Reference

## Purpose
The PostgreSQL Kubernetes Setup skill deploys and manages PostgreSQL databases on Kubernetes for persistent data storage.

## Features
- Automated PostgreSQL deployment
- Database schema migrations
- Comprehensive verification checks
- LearnFlow-specific table creation

## Usage Patterns
### Basic Deployment
```bash
bash scripts/deploy.sh
```

### Running Migrations
```bash
bash scripts/run_migrations.sh
```

### Verification
```bash
python scripts/verify.py
```

## Configuration Options
- Adjust database credentials in deploy.sh
- Modify persistence settings
- Change namespace if needed
- Customize resource limits

## LearnFlow Schema
The skill creates these tables for the LearnFlow application:
- `users` - User accounts and profiles
- `modules` - Course modules and curriculum
- `lessons` - Individual lessons within modules
- `exercises` - Practice exercises and challenges
- `user_progress` - Track student progress
- `submissions` - Student code submissions
- `ai_interactions` - AI tutoring session logs

## Dependencies
- Kubernetes cluster
- Helm 3+
- kubectl
- Sufficient cluster resources

## Best Practices
- Use persistent storage for production deployments
- Regularly backup important data
- Monitor database performance and connections
- Secure database access with proper authentication

## Integration with AI Agents
- Claude Code can deploy PostgreSQL with single command
- Goose can manage schemas and verify connectivity
- Provides persistent storage for application state
