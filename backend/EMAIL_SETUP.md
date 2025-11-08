# Email Configuration Guide for FIR Draft

## Setup Instructions

### 1. Gmail Setup (Recommended)

1. **Enable 2-Step Verification**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification if not already enabled

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select "Other (Custom name)" as device
   - Enter "Nyay Sahayak" as the name
   - Click "Generate"
   - Copy the 16-character password (remove spaces)

3. **Update .env file**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_16_character_app_password
   EMAIL_FROM=your_email@gmail.com
   EMAIL_FROM_NAME=Nyay Sahayak
   ```

### 2. Other Email Providers

#### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_password
EMAIL_FROM=your_email@outlook.com
EMAIL_FROM_NAME=Nyay Sahayak
```

#### Yahoo Mail
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@yahoo.com
EMAIL_FROM_NAME=Nyay Sahayak
```

#### Custom SMTP Server
```env
SMTP_SERVER=your_smtp_server.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
EMAIL_FROM=noreply@yourdomain.com
EMAIL_FROM_NAME=Nyay Sahayak
```

## Testing Email Configuration

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/send-fir-email" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP.",
    "email": "recipient@example.com",
    "user_name": "John Doe"
  }'
```

### Using PowerShell

```powershell
$body = @{
    query = "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
    email = "recipient@example.com"
    user_name = "John Doe"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/send-fir-email" -Method Post -Body $body -ContentType "application/json"
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/send-fir-email"
payload = {
    "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP.",
    "email": "recipient@example.com",
    "user_name": "John Doe"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Troubleshooting

### Error: "SMTP credentials not configured"
- Make sure `SMTP_USERNAME` and `SMTP_PASSWORD` are set in your `.env` file
- Restart your server after updating `.env` file

### Error: "Authentication failed"
- For Gmail: Make sure you're using an App Password, not your regular password
- Check that 2-Step Verification is enabled
- Verify the App Password is correct (no spaces)

### Error: "Connection timeout"
- Check your firewall settings
- Verify SMTP server and port are correct
- Try using port 465 with SSL instead of 587 with STARTTLS

### Email not received
- Check spam/junk folder
- Verify the recipient email address is correct
- Check server logs for error messages
- Test with a different email provider

## Security Notes

1. **Never commit `.env` file** to version control
2. **Use App Passwords** instead of regular passwords
3. **Keep credentials secure** and rotate them regularly
4. **Use environment variables** in production instead of `.env` file
5. **Enable SSL/TLS** for secure email transmission

## Production Recommendations

For production environments, consider:
- Using a dedicated email service (SendGrid, Mailgun, AWS SES)
- Implementing rate limiting for email sending
- Adding email queue system for reliability
- Logging email sending events
- Implementing retry mechanism for failed sends

