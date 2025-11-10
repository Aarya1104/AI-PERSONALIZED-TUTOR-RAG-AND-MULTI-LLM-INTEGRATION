# 🚀 Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Using Docker CLI

```bash
# Build the image
docker build -t ai-tutor-rag .

# Run the container
docker run -d \
  --name ai-tutor \
  -p 7866:7866 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  ai-tutor-rag

# View logs
docker logs -f ai-tutor

# Stop the container
docker stop ai-tutor
docker rm ai-tutor
```

## Access the Application

Once the container is running, access the application at:
- **Local:** http://localhost:7866
- **Network:** http://YOUR_SERVER_IP:7866

## First Time Setup

The first time you run the container, it will:
1. Start Ollama server
2. Download required models (phi3:mini and mistral:7b) - **This may take 10-15 minutes**
3. Start the Gradio web interface

**Be patient!** The initial model download can take some time depending on your internet connection.

## Configuration

### Port Configuration
- Default port: **7866** (Gradio interface)
- Ollama API: **11434** (internal, optionally exposed)

To change the port:
```bash
docker run -p YOUR_PORT:7866 ai-tutor-rag
```

### Volume Mounts
Persistent data is stored in:
- `./data` - ChromaDB database and conversation history
- `./uploads` - Uploaded documents
- `./models` - Downloaded models cache

### Resource Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB (for models and data)

**Recommended:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB

## Production Deployment

### Cloud Deployment Options

#### 1. **AWS EC2**
```bash
# Launch EC2 instance (t3.large or larger)
# SSH into instance
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repository and run
git clone YOUR_REPO_URL
cd ai-tutor-rag
docker-compose up -d
```

#### 2. **Google Cloud Platform (GCP)**
```bash
# Create a VM instance
gcloud compute instances create ai-tutor \
  --machine-type=e2-standard-4 \
  --zone=us-central1-a \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB

# SSH and install Docker
gcloud compute ssh ai-tutor
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Deploy
git clone YOUR_REPO_URL
cd ai-tutor-rag
docker-compose up -d
```

#### 3. **DigitalOcean**
```bash
# Create a Docker Droplet
# SSH into droplet (Docker pre-installed)
git clone YOUR_REPO_URL
cd ai-tutor-rag
docker-compose up -d
```

#### 4. **Azure**
```bash
# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name ai-tutor-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser

# SSH and setup
ssh azureuser@YOUR_VM_IP
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Deploy
git clone YOUR_REPO_URL
cd ai-tutor-rag
docker-compose up -d
```

### Reverse Proxy Setup (Optional)

For production with HTTPS, use Nginx:

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:7866;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Port already in use - change port in docker-compose.yml
# 2. Insufficient resources - increase Docker memory/CPU limits
```

### Models not downloading
```bash
# Enter container and manually pull
docker exec -it ai-tutor bash
ollama pull phi3:mini
ollama pull mistral:7b
```

### Application not accessible
```bash
# Check if container is running
docker ps

# Check if port is exposed
netstat -tulpn | grep 7866

# Check firewall rules
sudo ufw allow 7866
```

### Reset everything
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove images
docker rmi ai-tutor-rag

# Rebuild
docker-compose up -d --build
```

## Monitoring

### View real-time logs
```bash
docker-compose logs -f ai-tutor
```

### Check resource usage
```bash
docker stats ai-tutor
```

### Health check
```bash
curl http://localhost:7866/
```

## Scaling Considerations

For high-traffic scenarios:
1. Use a load balancer (Nginx, HAProxy)
2. Deploy multiple instances behind the load balancer
3. Use external vector database (Pinecone, Weaviate)
4. Consider GPU instances for faster inference

## Security

1. **Don't expose Ollama port (11434) publicly** unless needed
2. Use environment variables for sensitive data
3. Implement authentication (add to Gradio interface)
4. Use HTTPS in production
5. Keep Docker and dependencies updated

## Backup

```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Restore
tar -xzf backup-YYYYMMDD.tar.gz
```

## Update/Upgrade

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Verify models are downloaded
- Ensure sufficient resources
- Check network connectivity

---
**Happy Teaching! 🎓**
