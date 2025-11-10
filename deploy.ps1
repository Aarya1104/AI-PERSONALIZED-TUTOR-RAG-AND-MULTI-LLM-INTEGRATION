# AI Tutor RAG - Deployment Script (PowerShell)
# For Windows users

$ErrorActionPreference = "Stop"

Write-Host "🎓 AI Tutor RAG - Deployment Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if Docker is installed
function Test-Docker {
    try {
        docker --version | Out-Null
        Write-Host "✅ Docker is installed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
        exit 1
    }
}

# Function to check if Docker Compose is installed
function Test-DockerCompose {
    try {
        docker-compose --version | Out-Null
        Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "⚠️  Docker Compose is not installed. Falling back to Docker CLI." -ForegroundColor Yellow
        return $false
    }
}

# Show menu
function Show-Menu {
    Write-Host ""
    Write-Host "Select an option:" -ForegroundColor Cyan
    Write-Host "1) Build Docker image"
    Write-Host "2) Run with Docker Compose (recommended)"
    Write-Host "3) Run with Docker CLI"
    Write-Host "4) Stop all containers"
    Write-Host "5) View logs"
    Write-Host "6) Clean up (remove containers and images)"
    Write-Host "7) Rebuild and restart"
    Write-Host "8) Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter choice [1-8]"
    
    switch ($choice) {
        "1" { Build-Image }
        "2" { Run-Compose }
        "3" { Run-Docker }
        "4" { Stop-Containers }
        "5" { View-Logs }
        "6" { Clean-Up }
        "7" { Rebuild }
        "8" { exit 0 }
        default { 
            Write-Host "Invalid option" -ForegroundColor Red
            Show-Menu 
        }
    }
}

# Build Docker image
function Build-Image {
    Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
    docker build -t ai-tutor-rag:latest .
    Write-Host "✅ Image built successfully" -ForegroundColor Green
    Show-Menu
}

# Run with Docker Compose
function Run-Compose {
    if (Test-DockerCompose) {
        Write-Host "🚀 Starting with Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d
        Write-Host "✅ Container started" -ForegroundColor Green
        Write-Host "📱 Access the app at: http://localhost:7866" -ForegroundColor Cyan
        Write-Host "📊 View logs: docker-compose logs -f" -ForegroundColor Cyan
    }
    else {
        Write-Host "❌ Docker Compose not available" -ForegroundColor Red
    }
    Show-Menu
}

# Run with Docker CLI
function Run-Docker {
    Write-Host "🚀 Starting with Docker CLI..." -ForegroundColor Yellow
    
    # Stop existing container if running
    try {
        docker stop ai-tutor 2>$null
        docker rm ai-tutor 2>$null
    }
    catch {
        # Container doesn't exist, continue
    }
    
    # Create directories
    New-Item -ItemType Directory -Force -Path "data\chroma_db", "data\conversations", "uploads", "models" | Out-Null
    
    # Get current directory
    $currentDir = (Get-Location).Path
    
    # Run container
    docker run -d `
        --name ai-tutor `
        -p 7866:7866 `
        -v "${currentDir}\data:/app/data" `
        -v "${currentDir}\uploads:/app/uploads" `
        -v "${currentDir}\models:/app/models" `
        --restart unless-stopped `
        ai-tutor-rag:latest
    
    Write-Host "✅ Container started" -ForegroundColor Green
    Write-Host "📱 Access the app at: http://localhost:7866" -ForegroundColor Cyan
    Write-Host "📊 View logs: docker logs -f ai-tutor" -ForegroundColor Cyan
    Show-Menu
}

# Stop containers
function Stop-Containers {
    Write-Host "🛑 Stopping containers..." -ForegroundColor Yellow
    
    if (Test-DockerCompose) {
        docker-compose down 2>$null
    }
    
    try {
        docker stop ai-tutor 2>$null
        docker rm ai-tutor 2>$null
    }
    catch {
        # Container doesn't exist
    }
    
    Write-Host "✅ Containers stopped" -ForegroundColor Green
    Show-Menu
}

# View logs
function View-Logs {
    Write-Host "📊 Viewing logs..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to exit" -ForegroundColor Cyan
    Start-Sleep -Seconds 2
    
    try {
        $containers = docker ps --format "{{.Names}}"
        if ($containers -match "ai-tutor-rag") {
            docker-compose logs -f
        }
        elseif ($containers -match "ai-tutor") {
            docker logs -f ai-tutor
        }
        else {
            Write-Host "❌ No running containers found" -ForegroundColor Red
            Show-Menu
        }
    }
    catch {
        Write-Host "❌ Error viewing logs" -ForegroundColor Red
        Show-Menu
    }
}

# Cleanup
function Clean-Up {
    Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
    $confirm = Read-Host "This will remove all containers, images, and volumes. Continue? (y/N)"
    
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        try {
            docker-compose down -v 2>$null
        }
        catch {}
        
        try {
            docker stop ai-tutor 2>$null
            docker rm ai-tutor 2>$null
            docker rmi ai-tutor-rag:latest 2>$null
        }
        catch {}
        
        Write-Host "✅ Cleanup complete" -ForegroundColor Green
    }
    else {
        Write-Host "Cancelled" -ForegroundColor Yellow
    }
    Show-Menu
}

# Rebuild
function Rebuild {
    Write-Host "🔄 Rebuilding and restarting..." -ForegroundColor Yellow
    
    Stop-Containers
    Build-Image
    
    if (Test-DockerCompose) {
        docker-compose up -d --build
    }
    else {
        Run-Docker
    }
    
    Write-Host "✅ Rebuild complete" -ForegroundColor Green
    Show-Menu
}

# Main
function Main {
    Test-Docker
    Show-Menu
}

Main
