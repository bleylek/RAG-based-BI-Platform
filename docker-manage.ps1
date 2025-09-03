# Docker Management Script for RAG BI Platform
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

function Show-DockerStatus {
    Write-LogMessage "Checking container status..." -Color Cyan
    
    try {
        $containerStatus = docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Out-String
        Write-Host $containerStatus
        
        if (docker ps -q --filter "name=rag-bi-platform" --filter "status=running") {
            Write-LogMessage "RAG BI Platform is RUNNING" -Color Green
            Write-LogMessage "Access the application at: http://localhost:8080" -Color Cyan
            
            # Get container health
            $health = docker inspect --format='{{.State.Health.Status}}' rag-bi-platform 2>$null
            if ($health) {
                Write-LogMessage "Container health status: $health" -Color $(
                    if ($health -eq "healthy") { "Green" } 
                    elseif ($health -eq "starting") { "Yellow" } 
                    else { "Red" }
                )
            }
        } else {
            Write-LogMessage "RAG BI Platform is NOT RUNNING" -Color Yellow
        }
    }
    catch {
        Write-LogMessage "Error checking Docker status: $_" -Color Red
    }
}

function Start-App {
    Write-LogMessage "Starting RAG BI Platform..." -Color Cyan
    
    # Check if container exists
    $containerExists = docker ps -a --filter "name=rag-bi-platform" -q
    
    if ($containerExists) {
        # Container exists, just start it
        docker start rag-bi-platform
        if ($LASTEXITCODE -eq 0) {
            Write-LogMessage "Container started successfully!" -Color Green
            Write-LogMessage "Access the application at: http://localhost:8080" -Color Cyan
        } else {
            Write-LogMessage "Failed to start container." -Color Red
        }
    } else {
        # Container doesn't exist, need to run docker-compose up
        docker compose up -d
        if ($LASTEXITCODE -eq 0) {
            Write-LogMessage "Container created and started successfully!" -Color Green
            Write-LogMessage "Access the application at: http://localhost:8080" -Color Cyan
        } else {
            Write-LogMessage "Failed to create and start container." -Color Red
        }
    }
}

function Stop-App {
    Write-LogMessage "Stopping RAG BI Platform..." -Color Cyan
    
    docker compose down
    if ($LASTEXITCODE -eq 0) {
        Write-LogMessage "Container stopped successfully!" -Color Green
    } else {
        Write-LogMessage "Failed to stop container." -Color Red
    }
}

function Show-Logs {
    Write-LogMessage "Showing container logs (press Ctrl+C to exit):" -Color Cyan
    
    docker compose logs -f
}

function Show-Help {
    Write-Host @"
RAG BI Platform Docker Management Script
=======================================

Available Commands:

  status    - Check container status
  start     - Start the container
  stop      - Stop the container
  logs      - Show container logs
  help      - Show this help message

Example usage:
  .\docker-manage.ps1 start
  
"@ -ForegroundColor Cyan
}

# Main script logic
$command = $args[0]

if (-not $command) {
    # Default to showing status if no command provided
    Show-Help
    Show-DockerStatus
    exit 0
}

switch ($command.ToLower()) {
    "status" {
        Show-DockerStatus
    }
    "start" {
        Start-App
        # Wait a moment and check status
        Start-Sleep -Seconds 3
        Show-DockerStatus
    }
    "stop" {
        Stop-App
    }
    "logs" {
        Show-Logs
    }
    "help" {
        Show-Help
    }
    default {
        Write-LogMessage "Unknown command: $command" -Color Red
        Write-LogMessage "Use 'help' to see available commands." -Color Yellow
    }
}
