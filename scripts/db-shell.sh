set -e

echo "Opening PostgreSQL shell..."

docker compose exec -it db psql -U user -d mydatabase
