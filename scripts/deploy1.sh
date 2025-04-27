##### chmod +x scripts/deploy.sh###
#!/bin/bash

echo "Running as user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Directory listing:"
ls -la

set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "❌ Environment not provided!"
  exit 1
fi

echo "🚀 Starting deployment for environment: $ENVIRONMENT"

case $ENVIRONMENT in
  dev)
    echo "Running development deployment steps..."
    # Insert dev-specific deployment logic
    # Example:
    # cp conf/input.yaml /path/to/dev/config/
    ;;
  staging)
    echo "Running staging deployment steps..."
    # Insert staging-specific deployment logic
    # Example:
    # cp conf/input.yaml /path/to/staging/config/
    ;;
  prod)
    echo "Running production deployment steps..."
    # Insert prod-specific deployment logic
    # Example:
    # cp conf/input.yaml /path/to/prod/config/
    ;;
  *)
    echo "❌ Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

echo "✅ Deployment for $ENVIRONMENT completed!"
