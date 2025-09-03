# Enhanced Docker build script with optimizations and error handling
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue" # Makes PowerShell progress bars silent for better performance

# Timestamp for logging
function Get-Timestamp {
    return "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')]"
}

function Write-LogMessage {
    param (
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host "$(Get-Timestamp) $Message" -ForegroundColor $Color
}

Write-LogMessage "=== Starting RAG BI Platform Docker Build and Deployment ===" -Color Cyan

# Check Docker installation and status
try {
    Write-LogMessage "Checking Docker status..." -Color Gray
    docker info | Out-Null
}
catch {
    Write-LogMessage "Error: Docker is not running. Please start Docker Desktop and try again." -Color Red
    exit 1
}

# Önce temizlik yapalım
Write-LogMessage "Cleaning up existing containers..." -Color Yellow
docker-compose down 2>$null
docker rm -f rag-bi-platform 2>$null

# Create/check environment file
if (-not (Test-Path .env)) {
    Write-LogMessage "Warning: .env file not found. Creating from template..." -Color Yellow
    
    if (Test-Path .env.example) {
        Copy-Item -Path .env.example -Destination .env
        Write-LogMessage "Created .env from example template. Please update with your actual credentials." -Color Yellow
    }
    else {
        # Create minimal .env with essential variables
        @"
# Created automatically by build script
SECRET_KEY=please-change-this-to-a-secure-random-key
FLASK_ENV=production
"@ | Set-Content -Path .env -Encoding utf8
        Write-LogMessage "Created minimal .env file. Update with required configuration." -Color Yellow
    }
}

# Create required directories
Write-LogMessage "Setting up directory structure..." -Color Gray

# Start the build process
Write-LogMessage "Building Docker image..." -Color Cyan
docker compose build --progress=plain
$dirPaths = @(
    ".\rag_store\uploads",
    ".\instance"
)

foreach ($dir in $dirPaths) {
    if (-not (Test-Path $dir)) {
        Write-LogMessage "Creating directory: $dir" -Color Gray
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
}

# Enable BuildKit for faster builds
$env:DOCKER_BUILDKIT = 1
$env:COMPOSE_DOCKER_CLI_BUILD = 1

# Start with cleanup
Write-LogMessage "Cleaning Docker cache to ensure clean build..." -Color Gray
docker builder prune -f | Out-Null

# Pull base images first to ensure we have latest
Write-LogMessage "Pulling latest base images..." -Color Gray
docker pull python:3.10-slim

# Build the Docker image with optimizations
Write-LogMessage "Building Docker image with optimizations (this may take several minutes)..." -Color Green
docker compose build --progress=plain

# Check if build was successful
if ($LASTEXITCODE -eq 0) {
    Write-LogMessage "Docker build successful!" -Color Green
    
    # Stop existing containers
    Write-LogMessage "Stopping existing containers if any..." -Color Gray
    docker compose down
    
    # Start the container
    Write-LogMessage "Starting container..." -Color Green
    docker compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-LogMessage "Container is now running!" -Color Green
        Write-LogMessage "You can access your application at: http://localhost:8080" -Color Cyan
        
        # Check if application is healthy
        Write-LogMessage "Waiting for application to become healthy..." -Color Yellow
        
        $healthy = $false
        $retries = 10
        while (-not $healthy -and $retries -gt 0) {
            Start-Sleep -Seconds 5
            $status = docker inspect --format='{{.State.Health.Status}}' rag-bi-platform
            
            if ($status -eq "healthy") {
                $healthy = $true
                Write-LogMessage "Application is healthy and ready to use!" -Color Green
            }
            else {
                Write-LogMessage "Waiting for application to start... ($retries attempts left)" -Color Yellow
                $retries--
            }
        }
        
        if (-not $healthy) {
            Write-LogMessage "Warning: Application didn't report as healthy in the expected time." -Color Yellow
            Write-LogMessage "Check application logs for issues:" -Color Yellow
        }
        
        # Show logs
        Write-LogMessage "Showing container logs (press Ctrl+C to stop viewing logs):" -Color Yellow
        docker compose logs -f
    }
    else {
        Write-LogMessage "Failed to start Docker container." -Color Red
    }
}
else {
    Write-LogMessage "Docker build failed. See errors above for details." -Color Red
}
