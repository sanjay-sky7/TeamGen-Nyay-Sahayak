# PowerShell Test script for Nyay Sahayak API

$BASE_URL = "http://localhost:8000"

Write-Host "=== Testing Nyay Sahayak API ===" -ForegroundColor Green
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "${BASE_URL}/api/v1/health" -Method Get | ConvertTo-Json
Write-Host ""
Write-Host ""

# Test 2: Query Endpoint - Cybercrime
Write-Host "2. Testing Query Endpoint - Cybercrime..." -ForegroundColor Yellow
$body = @{
    query = "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
} | ConvertTo-Json

Invoke-RestMethod -Uri "${BASE_URL}/api/v1/query" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
Write-Host ""
Write-Host ""

# Test 3: Query Endpoint - Domestic Violence
Write-Host "3. Testing Query Endpoint - Domestic Violence..." -ForegroundColor Yellow
$body = @{
    query = "My husband has been physically abusing me and threatening me. What should I do?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "${BASE_URL}/api/v1/query" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
Write-Host ""
Write-Host ""

# Test 4: Query Endpoint - Theft
Write-Host "4. Testing Query Endpoint - Theft..." -ForegroundColor Yellow
$body = @{
    query = "Someone stole my wallet and phone from my bag in a crowded market."
} | ConvertTo-Json

Invoke-RestMethod -Uri "${BASE_URL}/api/v1/query" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json
Write-Host ""

