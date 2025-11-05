param(
    [string]$EnvFile = ".env"
)

if (-not (Test-Path $EnvFile)) {
    Write-Error "Environment file '$EnvFile' not found!"
    exit 1
}

Write-Host "Loading environment variables from: $EnvFile" -ForegroundColor Cyan

Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    
    # Skip empty lines and comments
    if ($line -eq "" -or $line.StartsWith("#")) {
        return
    }
    
    # Parse key=value pairs
    if ($line -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        
        # Remove surrounding quotes
        $value = $value -replace '^["'']|["'']$', ''
        
        # Set environment variable
        [Environment]::SetEnvironmentVariable($key, $value, [EnvironmentVariableTarget]::Process)
        Write-Host "  $key = $value" -ForegroundColor Green
    }
}

Write-Host "Environment variables loaded successfully!" -ForegroundColor Green