set -e

SERVICE=${1:-app}

echo "Showing logs for $SERVICE..."

docker compose logs -f $SERVICE
