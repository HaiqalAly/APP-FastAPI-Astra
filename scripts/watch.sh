set -e

COMPOSE_FILE="docker/docker-compose.yml"

echo "🔧 Ensuring services are up..."

docker compose -f $COMPOSE_FILE up -d

echo "🔭 Starting Docker Compose Watch..."
echo "Syncing: ../app -> /app"
echo "Rebuild trigger: ../pyproject.toml"

docker compose -f $COMPOSE_FILE watch