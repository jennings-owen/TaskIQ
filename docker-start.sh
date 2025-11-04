#!/bin/bash
# Bash script to start Docker containers for SynapseSquad application
# Usage: ./docker-start.sh

set -e

echo "=== SynapseSquad Docker Startup Script ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Docker is installed and running
echo -e "${YELLOW}Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed.${NC}"
    echo -e "${RED}Please install Docker from: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}ERROR: Docker daemon is not running.${NC}"
    echo -e "${RED}Please start Docker and try again.${NC}"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo -e "${GREEN}Docker found: $DOCKER_VERSION${NC}"

# Check if docker-compose is available
echo -e "${YELLOW}Checking Docker Compose...${NC}"
if ! docker compose version &> /dev/null; then
    echo -e "${RED}ERROR: Docker Compose is not available.${NC}"
    echo -e "${RED}Please install Docker Compose V2.${NC}"
    exit 1
fi

COMPOSE_VERSION=$(docker compose version)
echo -e "${GREEN}Docker Compose found: $COMPOSE_VERSION${NC}"

# Check if .env file exists
echo ""
echo -e "${YELLOW}Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}WARNING: .env file not found. Using default values.${NC}"
    echo -e "${YELLOW}For custom configuration, see ENV_FORMAT.md and create a .env file${NC}"
else
    echo -e "${GREEN}.env file found${NC}"
fi

# Stop any existing containers
echo ""
echo -e "${YELLOW}Stopping any existing containers...${NC}"
docker compose down 2>/dev/null || true

# Build and start containers
echo ""
echo -e "${YELLOW}Building and starting containers...${NC}"
echo -e "${CYAN}This may take a few minutes on first run...${NC}"
echo ""

if docker compose up --build -d; then
    echo ""
    echo -e "${GREEN}=== Containers started successfully! ===${NC}"
    echo ""
    echo -e "${CYAN}Services are available at:${NC}"
    echo -e "  Frontend: http://localhost:3000"
    echo -e "  Backend:  http://localhost:8000"
    echo -e "  API Docs: http://localhost:8000/docs"
    echo ""
    echo -e "${CYAN}Useful commands:${NC}"
    echo -e "  View logs:        docker compose logs -f"
    echo -e "  Stop containers:  docker compose down"
    echo -e "  Restart:          docker compose restart"
    echo -e "  View status:      docker compose ps"
    echo ""
    echo -e "${YELLOW}Checking container status...${NC}"
    docker compose ps
else
    echo ""
    echo -e "${RED}ERROR: Failed to start containers.${NC}"
    echo -e "${RED}Check the logs above for details.${NC}"
    echo -e "${YELLOW}You can also run: docker compose logs${NC}"
    exit 1
fi

