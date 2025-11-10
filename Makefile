.PHONY: build run stop restart logs clean help

# Variables
IMAGE_NAME=ai-tutor-rag
CONTAINER_NAME=ai-tutor
PORT=7866

help:
	@echo "AI Tutor RAG - Docker Management"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make build       - Build the Docker image"
	@echo "  make run         - Run the container (Docker Compose)"
	@echo "  make run-docker  - Run the container (Docker CLI)"
	@echo "  make stop        - Stop the container"
	@echo "  make restart     - Restart the container"
	@echo "  make logs        - View container logs"
	@echo "  make shell       - Open shell in running container"
	@echo "  make clean       - Remove container and image"
	@echo "  make rebuild     - Rebuild and restart"
	@echo "  make help        - Show this help message"

build:
	@echo "🔨 Building Docker image..."
	docker build -t $(IMAGE_NAME):latest .

run:
	@echo "🚀 Starting with Docker Compose..."
	docker-compose up -d
	@echo "✅ Container started"
	@echo "📱 Access at: http://localhost:$(PORT)"

run-docker:
	@echo "🚀 Starting with Docker CLI..."
	@mkdir -p data/chroma_db data/conversations uploads models
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		-v $$(pwd)/data:/app/data \
		-v $$(pwd)/uploads:/app/uploads \
		-v $$(pwd)/models:/app/models \
		--restart unless-stopped \
		$(IMAGE_NAME):latest
	@echo "✅ Container started"
	@echo "📱 Access at: http://localhost:$(PORT)"

stop:
	@echo "🛑 Stopping containers..."
	-docker-compose down 2>/dev/null || true
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true
	-docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "✅ Containers stopped"

restart: stop run

logs:
	@echo "📊 Viewing logs (Ctrl+C to exit)..."
	@docker-compose logs -f 2>/dev/null || docker logs -f $(CONTAINER_NAME)

shell:
	@echo "🐚 Opening shell in container..."
	@docker exec -it $(CONTAINER_NAME) /bin/bash

clean:
	@echo "🧹 Cleaning up..."
	@read -p "Remove all containers, images, and volumes? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v 2>/dev/null || true; \
		docker stop $(CONTAINER_NAME) 2>/dev/null || true; \
		docker rm $(CONTAINER_NAME) 2>/dev/null || true; \
		docker rmi $(IMAGE_NAME):latest 2>/dev/null || true; \
		echo "✅ Cleanup complete"; \
	else \
		echo "Cancelled"; \
	fi

rebuild: stop build run
	@echo "✅ Rebuild complete"

status:
	@echo "📊 Container Status:"
	@docker ps -a | grep -E "CONTAINER|$(CONTAINER_NAME)|ai-tutor" || echo "No containers found"
	@echo ""
	@echo "📊 Image Status:"
	@docker images | grep -E "REPOSITORY|$(IMAGE_NAME)" || echo "No images found"

test:
	@echo "🧪 Testing container health..."
	@curl -f http://localhost:$(PORT)/ && echo "✅ Health check passed" || echo "❌ Health check failed"
