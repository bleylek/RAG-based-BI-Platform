# Enhanced Docker cleanup script with detailed options
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue" # Makes PowerShell progress bars silent

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

Write-LogMessage "=== Docker Cleanup Script ===" -Color Cyan
Write-LogMessage "This script will clean up Docker resources to optimize your system." -Color Yellow

# Check if Docker is running
try {
    docker info | Out-Null
}
catch {
    Write-LogMessage "Error: Docker is not running. Please start Docker Desktop and try again." -Color Red
    exit 1
}

# Show current Docker disk usage
Write-LogMessage "Current Docker disk usage:" -Color Gray
docker system df

# Menu for cleanup options
$cleanupType = Read-Host @"

Choose cleanup level:
[1] Basic (default): Stop containers, remove unused containers/images (won't affect running services)
[2] Thorough: Basic + remove all build cache (recommended before builds)
[3] Complete: Thorough + remove unused volumes (CAUTION: may delete important data)
[4] Cancel: Exit without cleanup

Enter option (1-4)
"@

# Default to basic if no selection
if (-not $cleanupType) { $cleanupType = "1" }

switch ($cleanupType) {
    "1" {
        Write-LogMessage "Performing basic cleanup..." -Color Cyan
        
        # Stop running containers for this project
        Write-LogMessage "Stopping containers for this project..." -Color Gray
        docker compose down
        
        # Prune unused containers
        Write-LogMessage "Removing unused containers..." -Color Gray
        docker container prune -f
        
        # Prune unused images
        Write-LogMessage "Removing dangling images..." -Color Gray
        docker image prune -f
    }
    "2" {
        Write-LogMessage "Performing thorough cleanup..." -Color Cyan
        
        # Stop running containers for this project
        Write-LogMessage "Stopping containers for this project..." -Color Gray
        docker compose down
        
        # Prune unused containers
        Write-LogMessage "Removing unused containers..." -Color Gray
        docker container prune -f
        
        # Prune unused images
        Write-LogMessage "Removing dangling images..." -Color Gray
        docker image prune -f
        
        # Remove all builder cache
        Write-LogMessage "Clearing Docker build cache (this may take a moment)..." -Color Gray
        docker builder prune -f
    }
    "3" {
        Write-LogMessage "Performing complete cleanup..." -Color Cyan
        Write-LogMessage "CAUTION: This will remove volumes that might contain important data!" -Color Red
        $confirm = Read-Host "Are you sure you want to continue? (y/N)"
        
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-LogMessage "Complete cleanup cancelled." -Color Yellow
            exit 0
        }
        
        # Stop running containers for this project
        Write-LogMessage "Stopping containers for this project..." -Color Gray
        docker compose down -v
        
        # Prune unused containers
        Write-LogMessage "Removing unused containers..." -Color Gray
        docker container prune -f
        
        # Prune unused images
        Write-LogMessage "Removing unused images (including untagged)..." -Color Gray
        docker image prune -a -f
        
        # Prune volumes
        Write-LogMessage "Removing unused volumes..." -Color Gray
        docker volume prune -f
        
        # Remove all builder cache
        Write-LogMessage "Clearing Docker build cache..." -Color Gray
        docker builder prune -f
    }
    "4" {
        Write-LogMessage "Cleanup cancelled." -Color Yellow
        exit 0
    }
    default {
        Write-LogMessage "Invalid option. Exiting." -Color Red
        exit 1
    }
}

# Show disk space reclaimed
Write-LogMessage "Cleanup complete!" -Color Green
Write-LogMessage "Updated Docker disk usage:" -Color Gray
docker system df

Write-LogMessage "Docker system has been optimized." -Color Green
