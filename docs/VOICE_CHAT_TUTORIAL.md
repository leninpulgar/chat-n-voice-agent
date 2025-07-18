# Complete Voice Chat Setup Tutorial

This tutorial will guide you through setting up AI voice chat functionality using VAPI, so customers can call a phone number and talk to your AI assistant.

## Prerequisites

Before starting, ensure you have:
- ✅ Twilio account with valid credentials
- ✅ Working WhatsApp integration (from previous steps)
- ✅ Gemini API key configured
- ✅ Business PDF loaded in the system

## Step 1: Get VAPI API Key

### 1.1 Sign up for VAPI
1. Go to [VAPI.ai](https://vapi.ai)
2. Click "Sign Up" and create an account
3. Verify your email address
4. Complete the onboarding process

### 1.2 Get Your API Key
1. Log in to your VAPI dashboard
2. Navigate to **Settings** → **API Keys**
3. Click **"Create New API Key"**
4. Copy the API key (it looks like `vapi_xxx...`)
5. Store it securely - you'll need it for the next step

### 1.3 Update Environment Variables
Add your VAPI API key to your `.env` file:

```env
# Add this to your .env file
VAPI_API_KEY=vapi_your_actual_api_key_here
```

## Step 2: Get OpenAI API Key (Required for VAPI)

VAPI uses OpenAI's models for conversation, so you need an OpenAI API key.

### 2.1 Sign up for OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Create an account or log in
3. Navigate to **API Keys**
4. Click **"Create new secret key"**
5. Copy the key (starts with `sk-`)

### 2.2 Add to Environment
Add to your `.env` file:

```env
# Add this to your .env file
OPENAI_API_KEY=sk-your_actual_openai_key_here
```

## Step 3: Test Basic VAPI Connection

Let's create a simple test to verify everything is working:

### 3.1 Run the Setup Test

```bash
python test_vapi_setup.py
```

This script will:
- ✅ Check all required environment variables
- ✅ Test VAPI connection
- ✅ Load your business context from PDF
- ✅ Create a voice assistant
- ✅ Create a phone number
- ✅ Give you a phone number to test!

### 3.2 Expected Output

If successful, you should see:
```
🎉 Setup Complete!
📞 Your AI voice assistant is now available at: +1-XXX-XXX-XXXX
🎯 You can now call this number to test the voice chat!
```

## Step 4: Configure VAPI Dashboard

### 4.1 Access Your Dashboard
1. Go to [VAPI Dashboard](https://dashboard.vapi.ai)
2. Log in with your credentials
3. You should see your created assistant

### 4.2 Review Assistant Configuration
1. Click on your assistant name
2. Review the configuration:
   - **Model**: OpenAI GPT-4
   - **Voice**: ElevenLabs (default voice)
   - **System Message**: Contains your business information
   - **First Message**: Greeting message

### 4.3 Customize Voice (Optional)
1. In the assistant settings, go to **Voice**
2. Choose from available voices:
   - **Rachel**: Professional female voice
   - **Josh**: Professional male voice
   - **Antoni**: Warm male voice
   - **Bella**: Friendly female voice
3. Click **Save** to apply changes

## Step 5: Test Live Voice Calls

### 5.1 Make Your First Call
1. Call the phone number provided by the setup script
2. Wait for the AI to answer with the greeting
3. Try asking these questions:
   - "What services do you offer?"
   - "What are your business hours?"
   - "How can I contact you?"
   - "What are your prices?"

### 5.2 What to Expect
- **Response Time**: 1-3 seconds
- **Voice Quality**: Clear, natural speech
- **Accuracy**: Responses based on your PDF content
- **Conversation Flow**: Natural back-and-forth

### 5.3 Common Issues and Solutions

#### Issue: "The number you dialed is not available"
**Solution**: 
- Check that the phone number was created successfully
- Verify Twilio account has sufficient balance
- Ensure phone number is properly configured in VAPI

#### Issue: AI responds with generic answers
**Solution**:
- Verify business context was loaded properly
- Check the assistant's system message in VAPI dashboard
- Update the assistant with fresh business context

#### Issue: Poor voice quality or delays
**Solution**:
- Check internet connection
- Try different voice options in VAPI dashboard
- Verify OpenAI API key has sufficient credits

## Step 6: Monitor and Manage

### 6.1 View Call Logs
1. Go to VAPI Dashboard → **Calls**
2. Review recent call history
3. Listen to call recordings (if enabled)
4. Check call analytics

### 6.2 Update Business Information

When you update your business PDF:

```bash
# Run this script to update the voice assistant
python update_voice_assistant.py
```

### 6.3 Monitor Usage and Costs

#### VAPI Costs:
- **Voice calls**: ~$0.05-0.10 per minute
- **Phone number**: ~$1-2 per month

#### OpenAI Costs:
- **GPT-4**: ~$0.03 per 1K tokens
- **Average call**: ~$0.10-0.30

#### Twilio Costs:
- **Phone calls**: ~$0.01-0.05 per minute
- **Phone number**: ~$1 per month

## Step 7: Advanced Configuration

### 7.1 Customize Conversation Flow

Edit the assistant's system message to:
- Add specific conversation guidelines
- Include common Q&A patterns
- Set conversation limits
- Add escalation procedures

### 7.2 Add Multiple Languages

1. Create separate assistants for different languages
2. Use different phone numbers for each language
3. Update system messages with language-specific content

### 7.3 Integration with CRM

You can integrate call data with your CRM:

```python
# Example: Get call logs and process them
vapi = VAPIIntegration()
call_logs = vapi.get_call_logs(limit=50)

# Process and send to CRM
for call in call_logs:
    # Extract customer info and conversation
    # Send to your CRM system
    pass
```

## Step 8: Production Deployment

### 8.1 Get Production Phone Number

1. In VAPI Dashboard, go to **Phone Numbers**
2. Click **Buy New Number**
3. Choose your preferred area code
4. Select **Production** (not sandbox)
5. Purchase the number

### 8.2 Update Business Materials

- Add the phone number to your website
- Include it in business cards
- Add to email signatures
- Update marketing materials

### 8.3 Set Up Monitoring

1. **Call Quality Monitoring**:
   - Set up alerts for failed calls
   - Monitor response times
   - Track customer satisfaction

2. **Usage Monitoring**:
   - Set up billing alerts
   - Monitor API usage
   - Track call volume patterns

## Step 9: Troubleshooting Guide

### Common Problems and Solutions

#### Problem: "VAPI_API_KEY not found"
**Solution**: Add your VAPI API key to the `.env` file

#### Problem: "OpenAI API key invalid"
**Solution**: 
- Verify key is correct
- Check OpenAI account has credits
- Ensure key has proper permissions

#### Problem: "Assistant creation failed"
**Solution**:
- Check VAPI account limits
- Verify Twilio credentials
- Ensure business context is not too long

#### Problem: "Phone number creation failed"
**Solution**:
- Check Twilio account balance
- Verify Twilio credentials in VAPI
- Ensure phone number availability

### Debug Commands

```bash
# Test VAPI connection
python -c "from vapi_integration import VAPIIntegration; vapi = VAPIIntegration(); print(vapi.health_check())"

# Check assistants
python -c "from vapi_integration import VAPIIntegration; vapi = VAPIIntegration(); print(vapi.get_assistants())"

# Check phone numbers
python -c "from vapi_integration import VAPIIntegration; vapi = VAPIIntegration(); print(vapi.get_phone_numbers())"
```

## Step 10: Success Checklist

- [ ] VAPI account created and API key obtained
- [ ] OpenAI API key configured
- [ ] Environment variables set in `.env`
- [ ] Setup test script runs successfully
- [ ] Voice assistant created in VAPI
- [ ] Phone number provisioned
- [ ] Test call completed successfully
- [ ] AI responds with business-specific information
- [ ] Call quality is acceptable
- [ ] Dashboard monitoring set up
- [ ] Production phone number obtained (optional)
- [ ] Business materials updated with phone number

## Support and Resources

### Documentation
- [VAPI Documentation](https://docs.vapi.ai)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Twilio Voice Documentation](https://www.twilio.com/docs/voice)

### Community Support
- [VAPI Discord](https://discord.gg/vapi)
- [OpenAI Community](https://community.openai.com)
- [Twilio Community](https://www.twilio.com/community)

### Pricing Information
- [VAPI Pricing](https://vapi.ai/pricing)
- [OpenAI Pricing](https://openai.com/pricing)
- [Twilio Pricing](https://www.twilio.com/pricing)

---

🎉 **Congratulations!** You now have a fully functional AI voice assistant that customers can call to get information about your business!

📞 **Next Steps**: Test thoroughly, monitor usage, and consider integrating with your existing business systems.

💡 **Pro Tip**: Start with a few test calls to friends/family to ensure everything works perfectly before promoting the number to customers.
