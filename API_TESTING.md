# Nyay Sahayak API Testing Guide

## Quick Curl Commands

### 1. Send FIR Draft via Email

**Windows PowerShell:**
```powershell
$body = @{
    query = "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
    email = "user@example.com"
    user_name = "John Doe"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/send-fir-email" -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac/Windows (curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/send-fir-email" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP.",
    "email": "user@example.com",
    "user_name": "John Doe"
  }'
```

### 2. Query Endpoint (Main API using Google Gemini)

**Windows PowerShell:**
```powershell
$body = @{
    query = "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/query" -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac/Windows (curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"I was scammed online. Someone called me pretending to be from my bank and took my OTP.\"}"
```

**Using a JSON file:**
```bash
# Create request.json
echo '{"query": "I was scammed online"}' > request.json

# Make request
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d @request.json
```

### 2. Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### 3. Rebuild Index

```bash
curl -X POST "http://localhost:8000/api/v1/ingest"
```

## Example Queries

### Cybercrime
```json
{
  "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
}
```

### Domestic Violence
```json
{
  "query": "My husband has been physically abusing me and threatening me. What should I do?"
}
```

### Theft
```json
{
  "query": "Someone stole my wallet and phone from my bag in a crowded market."
}
```

### Fraud
```json
{
  "query": "I received a fake job offer and lost money. The company asked for money for training and then disappeared."
}
```

## Expected Response Format

```json
{
  "crime_type": "Cyber Fraud",
  "immediate_actions": [
    "Block your debit/credit card immediately",
    "Report to your bank's fraud helpline"
  ],
  "fir_steps": [
    "Visit nearest cyber police station",
    "File e-FIR at https://cybercrime.gov.in"
  ],
  "evidence_to_preserve": [
    "Screenshots of chats",
    "Transaction receipts",
    "Call recordings"
  ],
  "relevant_laws": [
    "IPC 420 – Cheating",
    "IT Act 66D – Impersonation"
  ]
}
```

## Using Postman or Insomnia

1. **Method**: POST
2. **URL**: `http://localhost:8000/api/v1/query`
3. **Headers**:
   - `Content-Type: application/json`
4. **Body** (raw JSON):
   ```json
   {
     "query": "Your legal situation description here"
   }
   ```

## Interactive API Documentation

Visit `http://localhost:8000/docs` in your browser for interactive Swagger UI documentation where you can test the API directly.

## Troubleshooting

1. **Make sure the server is running**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Check if the index is built**:
   ```bash
   python build_index.py
   ```

3. **Verify your Google API key is set**:
   - Check your `.env` file has `GOOGLE_API_KEY=your_key`
   - Or export it: `export GOOGLE_API_KEY=your_key`

4. **Check health endpoint**:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

