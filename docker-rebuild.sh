#!/bin/bash

if [ "$1" = "-Test" ]; then
    COMPOSE_FILE="docker-compose.test.yml"
    echo -e "\033[0;33mRebuilding test containers...\033[0m"
else
    COMPOSE_FILE="docker-compose.yml"
    echo -e "\033[0;33mRebuilding containers...\033[0m"
fi

echo -e "\033[0;90mStopping containers...\033[0m"
docker compose -f $COMPOSE_FILE down

echo -e "\033[0;90mRebuilding images...\033[0m"
docker compose -f $COMPOSE_FILE build --no-cache

echo -e "\033[0;90mStarting containers...\033[0m"
docker compose -f $COMPOSE_FILE up -d

echo ""
echo -e "\033[0;32mRebuild complete\033[0m"
echo ""
docker compose -f $COMPOSE_FILE ps

echo ""
echo -e "\033[0;90mFrontend: http://localhost:3000\033[0m"
echo -e "\033[0;90mBackend:  http://localhost:8000\033[0m"

