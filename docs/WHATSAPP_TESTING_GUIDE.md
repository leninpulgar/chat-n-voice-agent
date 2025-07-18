# WhatsApp Integration Testing Guide

This guide will help you test the WhatsApp integration step by step.

## Prerequisites

Before testing, ensure you have:
1. ✅ Twilio account with WhatsApp Sandbox enabled
2. ✅ Gemini API key configured
3. ✅ All dependencies installed
4. ✅ Environment variables set in `.env`

## Step 1: Test Basic Components

### 1.1 Test WhatsApp Bot Initialization
```bash
python -c "from whatsapp_integration import WhatsAppBot; bot = WhatsAppBot(); print('✅ WhatsApp bot works!')"
```

### 1.2 Test Gemini Agent
```bash
python -c "from gemini_agent import GeminiAgent; agent = GeminiAgent(); print('✅ Gemini agent works!')"
```

### 1.3 Test PDF Processing
```bash
python -c "from pdf_processor import PDFProcessor; proc = PDFProcessor('business_info.pdf'); print('✅ PDF processing works!')"
```

## Step 2: Test the Main Application

### 2.1 Start the Flask Application
```bash
python main.py
```

You should see output like:
```
INFO:pdf_processor:Business context loaded. Content length: XXXX characters
INFO:whatsapp_integration:WhatsApp Bot initialized successfully
INFO:main:All components initialized successfully
* Running on http://127.0.0.1:5000
```

### 2.2 Test Health Endpoint
In another terminal:
```bash
python -c "import requests; response = requests.get('http://localhost:5000/health'); print('Status:', response.status_code); print('Response:', response.json())"
```

Expected output:
```json
{
  "gemini": {
    "status": "healthy",
    "business_context_loaded": true,
    "context_length": XXXX,
    "conversation_history_length": 0,
    "model_name": "gemini-pro"
  },
  "whatsapp": {
    "status": "healthy",
    "account_sid": "YOUR_ACCOUNT_SID",
    "account_status": "active",
    "from_number": "whatsapp:+14155238886"
  }
}
```

## Step 3: Test WhatsApp Functionality

### 3.1 Test WhatsApp Message Sending
```bash
python test_whatsapp.py
```

Choose option 2 and enter your phone number when prompted.

### 3.2 Test API Message Sending
```bash
python test_whatsapp.py
```

Choose option 3 and enter your phone number when prompted.

### 3.3 Test Webhook Simulation
```bash
python test_whatsapp.py
```

Choose option 4 to simulate a webhook call.

## Step 4: Test Real WhatsApp Integration

### 4.1 Set up Ngrok Tunnel
In a new terminal:
```bash
python setup_ngrok.py
```

This will output something like:
```
Public URL: https://abcd1234.ngrok.io
WhatsApp Webhook URL: https://abcd1234.ngrok.io/whatsapp
```

### 4.2 Configure Twilio Webhook
1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Messaging → Settings → WhatsApp Sandbox**
3. In the "When a message comes in" field, enter:
# https://timberwolf-mastiff-9776.twil.io/demo-reply    <-- this is the default.
   ```
   https://your-ngrok-url.ngrok.io/whatsapp
   ```
4. Set HTTP method to **POST**
5. Click **Save**

### 4.3 Join WhatsApp Sandbox
1. In Twilio Console, find your sandbox join code (e.g., "join abc123")
2. Send this message to **+1 (415) 523-8886** on WhatsApp
3. You should receive a confirmation message

### 4.4 Test Live WhatsApp Integration
Send these test messages to **+1 (415) 523-8886**:

1. **"Hello"** - Should get a greeting
2. **"What services do you offer?"** - Should get business services info
3. **"What are your business hours?"** - Should get hours info
4. **"How can I contact you?"** - Should get contact info

## Step 5: Troubleshooting

### Common Issues and Solutions

#### 1. "Twilio credentials not found"
- Check your `.env` file has correct `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
- Ensure quotes are properly formatted
- Restart the application after updating `.env`

#### 2. "Invalid API key" for Gemini
- Verify `GEMINI_API_KEY` in `.env`
- Check the key hasn't expired
- Ensure proper quotation marks

#### 3. WhatsApp messages not receiving responses
- Check ngrok tunnel is running
- Verify webhook URL in Twilio Console
- Check Flask app logs for errors
- Ensure WhatsApp sandbox is properly joined

#### 4. "Connection refused" errors
- Ensure Flask app is running on port 5000
- Check firewall settings
- Verify ngrok is forwarding to correct port

#### 5. PDF not loading
- Check `business_info.pdf` exists
- Verify file permissions
- Try with a different PDF file

### Debug Commands

#### Check WhatsApp Bot Status
```bash
python -c "from whatsapp_integration import WhatsAppBot; bot = WhatsAppBot(); print(bot.get_health_status())"
```

#### Test AI Response
```bash
python -c "from gemini_agent import GeminiAgent; agent = GeminiAgent(); print(agent.generate_response('Hello'))"
```

#### Test PDF Content
```bash
python -c "from pdf_processor import PDFProcessor; proc = PDFProcessor('business_info.pdf'); print(proc.extract_text()[:200])"
```

## Step 6: Production Deployment

### For Production Use:
1. Replace ngrok with proper domain/hosting
2. Use production Twilio phone number (not sandbox)
3. Implement proper logging and monitoring
4. Add rate limiting and security measures
5. Use environment-specific configurations

### Security Considerations:
- Never commit `.env` file to version control
- Use webhook signature verification in production
- Implement proper authentication
- Monitor for abuse and rate limiting

## Testing Checklist

- [ ] WhatsApp bot initializes without errors
- [ ] Gemini agent responds to questions
- [ ] PDF content loads correctly
- [ ] Flask app starts successfully
- [ ] Health endpoint returns 200
- [ ] Manual WhatsApp message sending works
- [ ] API message sending works
- [ ] Webhook simulation works
- [ ] Ngrok tunnel starts correctly
- [ ] Twilio webhook configuration saved
- [ ] WhatsApp sandbox joined successfully
- [ ] Live WhatsApp messages get AI responses
- [ ] Different question types work correctly
- [ ] Error handling works as expected

## Support

If you encounter issues:
1. Check the logs in your Flask application
2. Verify all environment variables are set correctly
3. Test each component individually
4. Review Twilio debugger for webhook issues
5. Check Gemini API quotas and limits

Happy testing! 🚀
