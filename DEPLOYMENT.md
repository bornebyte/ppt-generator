# Deployment Guide

This guide covers various deployment options for the PPT Generator application.

## Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)

## Local Development

### Quick Start

```bash
# Clone and setup
git clone https://github.com/bornebyte/ppt-generator.git
cd ppt-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run development server
python main.py
```

### Using the CLI

```bash
# Make executable (if not already)
chmod +x pptgen

# Run development server
./pptgen

# Run production server
./pptgen -p

# Run on custom port
./pptgen -p 8000
```

## Production Deployment

### Using Gunicorn (Recommended)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your production values
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 main:app
   ```

### Gunicorn Configuration Options

- `-w 4`: Number of worker processes (2-4 x CPU cores)
- `-b 0.0.0.0:5000`: Bind address and port
- `--timeout 120`: Worker timeout (seconds)
- `--access-logfile logs/access.log`: Access log file
- `--error-logfile logs/error.log`: Error log file
- `--log-level info`: Logging level

### Using systemd (Linux)

Create a systemd service file at `/etc/systemd/system/pptgen.service`:

```ini
[Unit]
Description=PPT Generator Web Application
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/path/to/ppt-generator
Environment="PATH=/path/to/ppt-generator/venv/bin"
ExecStart=/path/to/ppt-generator/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 main:app

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable pptgen
sudo systemctl start pptgen
sudo systemctl status pptgen
```

## Docker Deployment

### Create Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  pptgen:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

### Build and Run

```bash
# Build image
docker build -t pptgen:latest .

# Run container
docker run -d -p 5000:5000 --name pptgen pptgen:latest

# Or use docker-compose
docker-compose up -d
```

## Cloud Deployment

### Deploy to Heroku

1. **Create Procfile**
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
   ```

2. **Create runtime.txt**
   ```
   python-3.11.0
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-pptgen-app
   git push heroku main
   heroku open
   ```

### Deploy to AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04 LTS)

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y
   
   # Clone repository
   git clone https://github.com/bornebyte/ppt-generator.git
   cd ppt-generator
   
   # Setup virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Nginx**
   
   Create `/etc/nginx/sites-available/pptgen`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

   Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/pptgen /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **Setup systemd service** (see systemd section above)

### Deploy to DigitalOcean App Platform

1. **Connect repository** to DigitalOcean App Platform

2. **Configure build settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 -b 0.0.0.0:8080 main:app`

3. **Set environment variables** in the dashboard

4. **Deploy**

### Deploy to Google Cloud Run

1. **Create Dockerfile** (see Docker section)

2. **Deploy**
   ```bash
   gcloud run deploy pptgen \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Deploy to Railway

1. **Connect GitHub repository** to Railway

2. **Configure**
   - Railway will auto-detect the Flask app
   - Set environment variables in dashboard

3. **Deploy** (automatic on git push)

## Reverse Proxy Setup

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/ppt-generator/static;
        expires 30d;
    }
}
```

### Apache Configuration

```apache
<VirtualHost *:80>
    ServerName your-domain.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
</VirtualHost>
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

## Monitoring and Logging

### Application Logs

```bash
# Create logs directory
mkdir -p logs

# Run with logging
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  main:app
```

### Monitoring with PM2

```bash
# Install PM2
npm install -g pm2

# Start application
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 main:app" --name pptgen

# Monitor
pm2 monit

# Logs
pm2 logs pptgen

# Auto-start on system boot
pm2 startup
pm2 save
```

## Performance Optimization

### Tips

1. **Use appropriate number of workers**
   ```
   workers = (2 x CPU cores) + 1
   ```

2. **Enable gzip compression** in Nginx
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

3. **Set up caching** for static files

4. **Use CDN** for static assets

5. **Monitor memory usage** and adjust workers accordingly

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data
- [ ] Enable CORS only for trusted domains
- [ ] Regular security audits

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Denied

```bash
# Fix file permissions
chmod +x pptgen
chmod +x install.sh
```

### Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Support

For issues and questions, please open an issue on GitHub.
