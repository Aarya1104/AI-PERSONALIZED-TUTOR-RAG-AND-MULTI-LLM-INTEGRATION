# 🚀 Quick Deployment Guide

## Prerequisites
- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- At least 8GB RAM available
- 20GB free disk space

## Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# Access at http://localhost:7866
```

**That's it!** Wait 10-15 minutes for models to download on first run.

## Option 2: Automated Deployment Scripts

### Windows (PowerShell)
```powershell
.\deploy.ps1
```

### Linux/Mac
```bash
chmod +x deploy.sh
./deploy.sh
```

## Option 3: Manual Docker Build

```bash
# Build
docker build -t ai-tutor-rag .

# Run
docker run -d -p 7866:7866 --name ai-tutor ai-tutor-rag
```

## Verification

1. Check logs: `docker-compose logs -f`
2. Wait for "Running on local URL: http://0.0.0.0:7866"
3. Open browser: http://localhost:7866

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build

# Clean everything
docker-compose down -v
docker rmi ai-tutor-rag
```

## Troubleshooting

**Can't access at localhost:7866?**
- Check if container is running: `docker ps`
- Check logs: `docker-compose logs`
- Check firewall/port settings

**Models not downloading?**
- This is normal on first run
- Wait 10-15 minutes for phi3:mini and mistral:7b
- Check logs to monitor progress

**Out of memory?**
- Increase Docker Desktop memory limit (Settings > Resources)
- Minimum 8GB recommended

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed cloud deployment instructions for:
- AWS EC2
- Google Cloud Platform
- Azure
- DigitalOcean
- Reverse proxy setup
- HTTPS configuration
- Scaling strategies

---

Need help? Check [DEPLOYMENT.md](DEPLOYMENT.md) for full documentation.
