import sys
import os
import requests
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from whatsapp_integration import WhatsAppBot

def test_whatsapp_send():
    """Test sending a WhatsApp message directly."""
    try:
        # Initialize WhatsApp bot
        bot = WhatsAppBot()
        
        # Test phone number (replace with your actual number)
        test_number = input("Enter your WhatsApp number (format: +1234567890): ")
        formatted_number = bot.format_phone_number(test_number)
        
        # Test message
        test_message = "Hello! This is a test message from your AI business assistant. How can I help you today?"
        
        # Send message
        print(f"Sending message to {formatted_number}...")
        message_sid = bot.send_message(formatted_number, test_message)
        
        print(f"Message sent successfully! Message SID: {message_sid}")
        
    except Exception as e:
        print(f"Error sending message: {e}")

def test_whatsapp_health():
    """Test WhatsApp bot health."""
    try:
        bot = WhatsAppBot()
        health = bot.get_health_status()
        print("WhatsApp Bot Health:")
        print(json.dumps(health, indent=2))
    except Exception as e:
        print(f"Error checking health: {e}")

def test_api_send():
    """Test sending WhatsApp message via API."""
    try:
        # Test the API endpoint
        url = "http://localhost:5000/send-whatsapp"
        
        # Get phone number from user
        phone_number = input("Enter your WhatsApp number (format: +1234567890): ")
        
        data = {
            "to_number": phone_number,
            "message": "Hello! This is a test message from your AI business assistant API."
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print("API message sent successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error testing API: {e}")

def test_webhook_simulation():
    """Simulate a WhatsApp webhook call."""
    try:
        url = "http://localhost:5000/whatsapp"
        
        # Simulate Twilio webhook data
        data = {
            'From': 'whatsapp:+1234567890',
            'To': 'whatsapp:+14155238886',
            'Body': 'What are your business hours?',
            'MessageSid': 'SM1234567890abcdef',
            'AccountSid': 'AC1234567890abcdef',
            'ProfileName': 'Test User'
        }
        
        print("Simulating webhook call...")
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("Webhook simulation successful!")
            print("Response:")
            print(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error simulating webhook: {e}")

def main():
    """Main testing function."""
    print("=== WhatsApp Integration Testing ===\n")
    
    while True:
        print("\nChoose a test option:")
        print("1. Test WhatsApp Health")
        print("2. Send WhatsApp Message Directly")
        print("3. Send WhatsApp Message via API")
        print("4. Simulate Webhook Call")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_whatsapp_health()
        elif choice == '2':
            test_whatsapp_send()
        elif choice == '3':
            test_api_send()
        elif choice == '4':
            test_webhook_simulation()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
