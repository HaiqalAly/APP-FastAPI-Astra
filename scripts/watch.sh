set -e

echo "🔧 Ensuring services are up..."

docker compose up -d --build

echo "🔭 Starting Docker Compose Watch..."
echo "Syncing: ./app -> /app"
echo "Rebuild trigger: ./pyproject.toml"

docker compose watch