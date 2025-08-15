# Deployment Guide

This guide covers different ways to deploy the Car Price Predictor application.

## Prerequisites

- Node.js 18+ installed
- Docker (for containerized deployment)
- Git

## Method 1: Local Development

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd car-price-predictor
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

## Method 2: Docker Deployment

### Using Docker Compose (Recommended)

1. Build and run with Docker Compose:
```bash
npm run docker:compose
```

2. Access the application at http://localhost:3000

3. Stop the application:
```bash
npm run docker:compose:down
```

### Manual Docker Commands

1. Build the Docker image:
```bash
npm run docker:build
```

2. Run the container:
```bash
npm run docker:run
```

3. Or run with custom port:
```bash
docker run -p 8080:3000 car-price-predictor
```

## Method 3: Vercel Deployment

### Automatic Deployment

1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your repository
4. Vercel will automatically detect Next.js and deploy

### Manual Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts to configure your deployment

## Method 4: Production Server Deployment

### Using PM2

1. Build the application:
```bash
npm run build
```

2. Install PM2:
```bash
npm install -g pm2
```

3. Start the application:
```bash
pm2 start npm --name "car-price-predictor" -- start
```

4. Save PM2 configuration:
```bash
pm2 save
pm2 startup
```

### Using Systemd

1. Create a systemd service file `/etc/systemd/system/car-price-predictor.service`:
```ini
[Unit]
Description=Car Price Predictor
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/car-price-predictor
ExecStart=/usr/bin/npm start
Restart=always
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

2. Enable and start the service:
```bash
sudo systemctl enable car-price-predictor
sudo systemctl start car-price-predictor
```

## Environment Variables

Create a `.env.local` file for local development:

```env
NODE_ENV=development
NEXT_TELEMETRY_DISABLED=1
```

For production, set these environment variables:

```env
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

## API Configuration

The application is configured to use the API at `http://103.47.224.217:8080`. 

To change the API endpoint:

1. Edit `src/lib/api.ts`
2. Update the `API_BASE_URL` constant
3. Rebuild and redeploy

## Health Check

The application includes a health check endpoint at `/api/health` that returns:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 123.456,
  "environment": "production"
}
```

## Monitoring

### Docker Health Check

The Docker Compose configuration includes health checks:

```bash
# Check container health
docker ps

# View health check logs
docker logs car-price-predictor
```

### Application Monitoring

1. Check application logs:
```bash
# Docker
docker logs car-price-predictor

# PM2
pm2 logs car-price-predictor

# Systemd
sudo journalctl -u car-price-predictor -f
```

2. Monitor application metrics:
```bash
# PM2
pm2 monit

# Docker stats
docker stats car-price-predictor
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 3000
   lsof -i :3000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Docker build fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -t car-price-predictor .
   ```

3. **API connection issues**
   - Check if the API server is running
   - Verify the API URL in `src/lib/api.ts`
   - Check network connectivity

4. **Memory issues**
   ```bash
   # Increase Node.js memory limit
   export NODE_OPTIONS="--max-old-space-size=4096"
   ```

### Performance Optimization

1. **Enable compression** (if using nginx):
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Set up caching headers**:
```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Use CDN** for static assets in production

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to version control
2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Configure CORS properly if needed
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: All inputs are validated on both client and server side

## Backup and Recovery

1. **Database Backup** (if applicable):
```bash
# Example for PostgreSQL
pg_dump database_name > backup.sql
```

2. **Application Backup**:
```bash
# Backup application files
tar -czf car-price-predictor-backup.tar.gz /path/to/app
```

3. **Docker Image Backup**:
```bash
# Save Docker image
docker save car-price-predictor > car-price-predictor.tar

# Load Docker image
docker load < car-price-predictor.tar
```

## Support

For deployment issues:

1. Check the application logs
2. Verify environment configuration
3. Test API connectivity
4. Review this deployment guide
5. Open an issue in the GitHub repository

## Additional Resources

- [Next.js Deployment Documentation](https://nextjs.org/docs/deployment)
- [Docker Documentation](https://docs.docker.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)
