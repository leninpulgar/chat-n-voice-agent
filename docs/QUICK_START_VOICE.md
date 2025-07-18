# Quick Start Guide: Voice Chat Setup

## 🚀 Get Voice Chat Running in 10 Minutes

### Step 1: Get API Keys (5 minutes)

1. **VAPI Account**:
   - Go to [vapi.ai](https://vapi.ai) → Sign up
   - Get API key from Settings → API Keys
   - Add to `.env`: `VAPI_API_KEY=vapi_your_key_here`

2. **OpenAI Account**:
   - Go to [platform.openai.com](https://platform.openai.com) → Sign up
   - Get API key from API Keys section
   - Add to `.env`: `OPENAI_API_KEY=sk-your_key_here`

### Step 2: Run Setup Script (3 minutes)

```bash
python test_vapi_setup.py
```

Choose option 1 (Test full setup). This will:
- ✅ Check your API keys
- ✅ Create voice assistant
- ✅ Get phone number
- ✅ Show you the phone number to call!

### Step 3: Test It! (2 minutes)

Call the phone number provided and ask:
- "What services do you offer?"
- "What are your business hours?"
- "How can I contact you?"

## 🎯 That's It!

Your customers can now call your AI assistant!

## 📞 Example Phone Number Output:
```
🎉 Setup Complete!
📞 Your AI voice assistant is now available at: +1-555-123-4567
🎯 You can now call this number to test the voice chat!
```

## 🔧 If Something Goes Wrong:

### Problem: Missing API keys
**Solution**: Check your `.env` file has both `VAPI_API_KEY` and `OPENAI_API_KEY`

### Problem: Setup script fails
**Solution**: Make sure you have:
- Valid Twilio credentials (from WhatsApp setup)
- business_info.pdf in the project directory
- Internet connection

### Problem: Phone number doesn't work
**Solution**: 
- Check Twilio account balance
- Verify phone number was created in VAPI dashboard
- Wait 1-2 minutes after setup

## 💡 Next Steps:

1. **Test thoroughly** - Call multiple times with different questions
2. **Check VAPI dashboard** - Monitor call logs and analytics
3. **Update business info** - Run `python update_voice_assistant.py` when needed
4. **Get production number** - Buy a permanent number in VAPI dashboard

## 💰 Estimated Costs:

- **Testing**: ~$0.50-1.00 for initial setup and testing
- **Production**: ~$0.10-0.30 per call
- **Monthly**: ~$3-5 for phone number + usage

## 🆘 Need Help?

1. Check `VOICE_CHAT_TUTORIAL.md` for detailed instructions
2. Run health check: `python -c "from vapi_integration import VAPIIntegration; vapi = VAPIIntegration(); print(vapi.health_check())"`
3. Check logs in VAPI dashboard

---

**Ready to go live?** Add the phone number to your website and business cards! 🎉
