#!/usr/bin/env python3
"""
VAPI Voice Testing Script
Test different voice configurations with your VAPI integration
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vapi_integration import VAPIIntegration
from pdf_processor import PDFProcessor
import json

# Popular voice configurations
VOICE_OPTIONS = {
    "1": {
        "name": "Rachel (Female, Professional)",
        "provider": "11labs",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "stability": "0.5",
        "similarity_boost": "0.8"
    },
    "2": {
        "name": "Adam (Male, Deep)",
        "provider": "11labs", 
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "stability": "0.6",
        "similarity_boost": "0.8"
    },
    "3": {
        "name": "Bella (Female, Friendly)",
        "provider": "11labs",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "stability": "0.4",
        "similarity_boost": "0.9"
    },
    "4": {
        "name": "Antoni (Male, Mature)",
        "provider": "11labs",
        "voice_id": "ErXwobaYiN019PkySvjV",
        "stability": "0.7",
        "similarity_boost": "0.8"
    },
    "5": {
        "name": "OpenAI Alloy",
        "provider": "openai",
        "voice_id": "alloy"
    },
    "6": {
        "name": "OpenAI Nova",
        "provider": "openai",
        "voice_id": "nova"
    }
}

def set_voice_config(choice):
    """Set environment variables for voice configuration."""
    if choice not in VOICE_OPTIONS:
        print("Invalid choice!")
        return False
    
    config = VOICE_OPTIONS[choice]
    
    # Set environment variables
    os.environ['VAPI_VOICE_PROVIDER'] = config['provider']
    os.environ['VAPI_VOICE_ID'] = config['voice_id']
    
    if config['provider'] == '11labs':
        os.environ['VAPI_VOICE_STABILITY'] = config['stability']
        os.environ['VAPI_VOICE_SIMILARITY_BOOST'] = config['similarity_boost']
    
    print(f"✅ Voice configuration set to: {config['name']}")
    return True

def create_test_assistant(voice_choice):
    """Create a test assistant with the selected voice."""
    try:
        # Load business context
        pdf_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'business_info.pdf')
        pdf_processor = PDFProcessor(pdf_path)
        business_content = pdf_processor.extract_text()
        
        # Create VAPI integration
        vapi = VAPIIntegration()
        
        # Create assistant with selected voice
        assistant_info = vapi.create_assistant(
            business_context=business_content,
            business_name=f"TechSolutions Pro (Voice Test {voice_choice})"
        )
        
        if assistant_info:
            print(f"✅ Test assistant created successfully!")
            print(f"   Assistant ID: {assistant_info.get('id')}")
            print(f"   Voice: {VOICE_OPTIONS[voice_choice]['name']}")
            return assistant_info
        else:
            print("❌ Failed to create test assistant")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test assistant: {e}")
        return None

def main():
    print("🎤 VAPI Voice Configuration Tester")
    print("=" * 50)
    
    print("\nAvailable Voice Options:")
    for key, config in VOICE_OPTIONS.items():
        print(f"{key}. {config['name']}")
    
    print("\nWhat would you like to do?")
    print("A. Test a voice by creating an assistant")
    print("B. Just show voice configuration")
    print("C. Exit")
    
    choice = input("\nEnter your choice (A/B/C): ").upper()
    
    if choice == 'A':
        voice_choice = input(f"\nChoose a voice (1-{len(VOICE_OPTIONS)}): ")
        
        if voice_choice in VOICE_OPTIONS:
            print(f"\n🎯 Testing voice: {VOICE_OPTIONS[voice_choice]['name']}")
            
            # Set voice configuration
            if set_voice_config(voice_choice):
                # Create test assistant
                assistant_info = create_test_assistant(voice_choice)
                
                if assistant_info:
                    print("\n🎉 Voice test complete!")
                    print("The assistant has been created with your selected voice.")
                    print("Note: You would need a phone number to test the actual voice.")
                    
                    # Ask if user wants to delete the test assistant
                    delete = input("\nDelete the test assistant? (y/N): ").lower()
                    if delete == 'y':
                        try:
                            vapi = VAPIIntegration()
                            if vapi.delete_assistant(assistant_info.get('id')):
                                print("✅ Test assistant deleted")
                            else:
                                print("❌ Failed to delete test assistant")
                        except Exception as e:
                            print(f"❌ Error deleting assistant: {e}")
        else:
            print("❌ Invalid voice choice")
    
    elif choice == 'B':
        voice_choice = input(f"\nChoose a voice to view configuration (1-{len(VOICE_OPTIONS)}): ")
        
        if voice_choice in VOICE_OPTIONS:
            config = VOICE_OPTIONS[voice_choice]
            print(f"\n📋 Voice Configuration for: {config['name']}")
            print("-" * 40)
            
            if config['provider'] == '11labs':
                print(f"Provider: {config['provider']}")
                print(f"Voice ID: {config['voice_id']}")
                print(f"Stability: {config['stability']}")
                print(f"Similarity Boost: {config['similarity_boost']}")
                
                print(f"\n🔧 To use this voice, add to your .env file:")
                print(f"VAPI_VOICE_PROVIDER={config['provider']}")
                print(f"VAPI_VOICE_ID={config['voice_id']}")
                print(f"VAPI_VOICE_STABILITY={config['stability']}")
                print(f"VAPI_VOICE_SIMILARITY_BOOST={config['similarity_boost']}")
            
            else:  # OpenAI or other providers
                print(f"Provider: {config['provider']}")
                print(f"Voice: {config['voice_id']}")
                
                print(f"\n🔧 To use this voice, add to your .env file:")
                print(f"VAPI_VOICE_PROVIDER={config['provider']}")
                print(f"VAPI_VOICE_ID={config['voice_id']}")
        else:
            print("❌ Invalid voice choice")
    
    elif choice == 'C':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
