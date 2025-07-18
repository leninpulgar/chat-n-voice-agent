import subprocess
import time
import requests
import json
from pyngrok import ngrok
import os
from dotenv import load_dotenv

def setup_ngrok():
    """Set up ngrok tunnel for WhatsApp webhook testing."""
    load_dotenv()
    
    # Get ngrok auth token if available
    ngrok_token = os.getenv('NGROK_AUTH_TOKEN')
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)
    
    # Start ngrok tunnel
    print("Starting ngrok tunnel...")
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    
    # Print webhook URL
    webhook_url = f"{public_url}/whatsapp"
    print(f"WhatsApp Webhook URL: {webhook_url}")
    
    print("\nTo configure your Twilio WhatsApp webhook:")
    print("1. Go to https://console.twilio.com/")
    print("2. Navigate to Messaging > Settings > WhatsApp Sandbox")
    print("3. Set the webhook URL to:")
    print(f"   {webhook_url}")
    print("4. Save the configuration")
    
    # Keep the tunnel alive
    try:
        print("\nNgrok tunnel is running. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down ngrok tunnel...")
        ngrok.disconnect(public_url)
        ngrok.kill()

if __name__ == "__main__":
    setup_ngrok()
