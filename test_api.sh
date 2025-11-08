#!/bin/bash
# Test script for Nyay Sahayak API

BASE_URL="http://localhost:8000"

echo "=== Testing Nyay Sahayak API ==="
echo ""

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -X GET "${BASE_URL}/api/v1/health" | python -m json.tool
echo ""
echo ""

# Test 2: Query Endpoint - Cybercrime
echo "2. Testing Query Endpoint - Cybercrime..."
curl -X POST "${BASE_URL}/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
  }' | python -m json.tool
echo ""
echo ""

# Test 3: Query Endpoint - Domestic Violence
echo "3. Testing Query Endpoint - Domestic Violence..."
curl -X POST "${BASE_URL}/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "My husband has been physically abusing me and threatening me. What should I do?"
  }' | python -m json.tool
echo ""
echo ""

# Test 4: Query Endpoint - Theft
echo "4. Testing Query Endpoint - Theft..."
curl -X POST "${BASE_URL}/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Someone stole my wallet and phone from my bag in a crowded market."
  }' | python -m json.tool
echo ""

