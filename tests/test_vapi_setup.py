#!/usr/bin/env python3
"""
Enhanced VAPI Test Script
This script tests the complete VAPI integration setup
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from vapi_integration import VAPIIntegration
from pdf_processor import PDFProcessor

def test_vapi_setup():
    """Test the complete VAPI setup process."""
    
    print("🎯 Testing VAPI Voice Chat Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))
    
    # Check required environment variables
    required_vars = [
        'VAPI_API_KEY',
        'OPENAI_API_KEY',
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN'
    ]
    
    print("\n📋 Checking Environment Variables...")
    missing_vars = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: Present")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please add these to your .env file and try again.")
        return False
    
    # Test VAPI connection
    print("\n🔌 Testing VAPI Connection...")
    try:
        vapi = VAPIIntegration()
        health = vapi.health_check()
        if health.get('status') == 'healthy':
            print("✅ VAPI connection successful")
        else:
            print(f"❌ VAPI connection failed: {health}")
            return False
    except Exception as e:
        print(f"❌ VAPI initialization failed: {e}")
        return False
    
    # Load business context
    print("\n📄 Loading Business Context...")
    try:
        pdf_processor = PDFProcessor(os.path.join(os.path.dirname(__file__), '..', 'examples', 'business_info.pdf'))
        business_content = pdf_processor.extract_text()
        print(f"✅ Business context loaded ({len(business_content)} characters)")
    except Exception as e:
        print(f"❌ Failed to load business context: {e}")
        return False
    
    # Test creating assistant
    print("\n🤖 Creating Voice Assistant...")
    try:
        assistant_info = vapi.create_assistant(
            business_context=business_content,
            business_name="TechSolutions Pro"
        )
        
        if assistant_info:
            assistant_id = assistant_info.get('id')
            print(f"✅ Assistant created successfully!")
            print(f"   Assistant ID: {assistant_id}")
            
            # Test creating phone number
            print("\n📞 Creating Phone Number...")
            phone_info = vapi.create_phone_number(assistant_id)
            
            if phone_info:
                phone_number = phone_info.get('number')
                print(f"✅ Phone number created successfully!")
                print(f"   Phone Number: {phone_number}")
                
                print("\n🎉 Setup Complete!")
                print("=" * 50)
                print(f"📞 Your AI voice assistant is now available at: {phone_number}")
                print("🎯 You can now call this number to test the voice chat!")
                
                return True
            else:
                print("❌ Failed to create phone number")
                return False
        else:
            print("❌ Failed to create assistant")
            return False
            
    except Exception as e:
        print(f"❌ Error in setup process: {e}")
        return False

def cleanup_test_resources():
    """Clean up any test resources created."""
    print("\n🧹 Cleaning up test resources...")
    
    try:
        vapi = VAPIIntegration()
        
        # Get all assistants
        assistants = vapi.get_assistants()
        if assistants:
            print(f"Found {len(assistants)} assistants")
            
            # Delete test assistants (optional)
            for assistant in assistants:
                if "TechSolutions Pro" in assistant.get('name', ''):
                    print(f"Deleting assistant: {assistant.get('id')}")
                    vapi.delete_assistant(assistant.get('id'))
        
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

def main():
    """Main function to run the test."""
    
    print("Welcome to the VAPI Voice Chat Setup Test!")
    print("This script will help you set up and test your voice assistant.")
    print()
    
    choice = input("What would you like to do?\n1. Test full setup\n2. Cleanup test resources\n3. Exit\nEnter choice (1-3): ")
    
    if choice == "1":
        success = test_vapi_setup()
        if success:
            print("\n🎊 Congratulations! Your voice chat is ready!")
            print("📖 Check the tutorial for next steps.")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    
    elif choice == "2":
        cleanup_test_resources()
    
    elif choice == "3":
        print("👋 Goodbye!")
    
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
