#!/bin/bash
# Build and Deploy Script for AI Tutor RAG

set -e

echo "🎓 AI Tutor RAG - Deployment Script"
echo "===================================="
echo ""

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    echo "✅ Docker is installed"
}

# Function to check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo "⚠️  Docker Compose is not installed. Falling back to Docker CLI."
        return 1
    fi
    echo "✅ Docker Compose is installed"
    return 0
}

# Menu
show_menu() {
    echo ""
    echo "Select an option:"
    echo "1) Build Docker image"
    echo "2) Run with Docker Compose (recommended)"
    echo "3) Run with Docker CLI"
    echo "4) Stop all containers"
    echo "5) View logs"
    echo "6) Clean up (remove containers and images)"
    echo "7) Rebuild and restart"
    echo "8) Exit"
    echo ""
    read -p "Enter choice [1-8]: " choice
    
    case $choice in
        1) build_image ;;
        2) run_compose ;;
        3) run_docker ;;
        4) stop_containers ;;
        5) view_logs ;;
        6) cleanup ;;
        7) rebuild ;;
        8) exit 0 ;;
        *) echo "Invalid option"; show_menu ;;
    esac
}

# Build Docker image
build_image() {
    echo "🔨 Building Docker image..."
    docker build -t ai-tutor-rag:latest .
    echo "✅ Image built successfully"
    show_menu
}

# Run with Docker Compose
run_compose() {
    if check_docker_compose; then
        echo "🚀 Starting with Docker Compose..."
        docker-compose up -d
        echo "✅ Container started"
        echo "📱 Access the app at: http://localhost:7866"
        echo "📊 View logs: docker-compose logs -f"
    else
        echo "❌ Docker Compose not available"
    fi
    show_menu
}

# Run with Docker CLI
run_docker() {
    echo "🚀 Starting with Docker CLI..."
    
    # Stop existing container if running
    docker stop ai-tutor 2>/dev/null || true
    docker rm ai-tutor 2>/dev/null || true
    
    # Create directories
    mkdir -p data/chroma_db data/conversations uploads models
    
    # Run container
    docker run -d \
        --name ai-tutor \
        -p 7866:7866 \
        -v "$(pwd)/data:/app/data" \
        -v "$(pwd)/uploads:/app/uploads" \
        -v "$(pwd)/models:/app/models" \
        --restart unless-stopped \
        ai-tutor-rag:latest
    
    echo "✅ Container started"
    echo "📱 Access the app at: http://localhost:7866"
    echo "📊 View logs: docker logs -f ai-tutor"
    show_menu
}

# Stop containers
stop_containers() {
    echo "🛑 Stopping containers..."
    
    if check_docker_compose; then
        docker-compose down
    fi
    
    docker stop ai-tutor 2>/dev/null || true
    docker rm ai-tutor 2>/dev/null || true
    
    echo "✅ Containers stopped"
    show_menu
}

# View logs
view_logs() {
    echo "📊 Viewing logs..."
    echo "Press Ctrl+C to exit"
    sleep 2
    
    if docker ps | grep -q ai-tutor-rag; then
        docker-compose logs -f
    elif docker ps | grep -q ai-tutor; then
        docker logs -f ai-tutor
    else
        echo "❌ No running containers found"
        show_menu
    fi
}

# Cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    read -p "This will remove all containers, images, and volumes. Continue? (y/N): " confirm
    
    if [[ $confirm == [yY] ]]; then
        docker-compose down -v 2>/dev/null || true
        docker stop ai-tutor 2>/dev/null || true
        docker rm ai-tutor 2>/dev/null || true
        docker rmi ai-tutor-rag:latest 2>/dev/null || true
        echo "✅ Cleanup complete"
    else
        echo "Cancelled"
    fi
    show_menu
}

# Rebuild
rebuild() {
    echo "🔄 Rebuilding and restarting..."
    
    stop_containers
    build_image
    
    if check_docker_compose; then
        docker-compose up -d --build
    else
        run_docker
    fi
    
    echo "✅ Rebuild complete"
    show_menu
}

# Main
main() {
    check_docker
    show_menu
}

main
