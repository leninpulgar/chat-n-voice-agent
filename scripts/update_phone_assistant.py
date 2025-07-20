#!/usr/bin/env python3
"""
Update VAPI Phone Number Assistant
This script updates which assistant is assigned to a phone number
"""

import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vapi_integration import VAPIIntegration

def update_phone_assistant(phone_id, new_assistant_id):
    """Update phone number to use a different assistant."""
    try:
        vapi = VAPIIntegration()
        
        # Update the phone number configuration
        update_data = {
            "assistantId": new_assistant_id
        }
        
        response = requests.patch(
            f"{vapi.base_url}/phone-number/{phone_id}",
            headers=vapi.headers,
            json=update_data
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully updated phone number {phone_id} to use assistant {new_assistant_id}")
            return response.json()
        else:
            print(f"❌ Failed to update phone number: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error updating phone number: {e}")
        return None

def main():
    print("🔄 VAPI Phone Number Assistant Update")
    print("=" * 50)
    
    # Current configuration
    current_phone_id = "08683264-de30-47d3-9c52-1af12d9e1dc7"
    current_assistant_id = "fdb0411f-ebd1-4481-903e-fb235d4d2998"  # Female voice
    new_assistant_id = "8ff1ebe8-9fdf-4e43-b87a-614523d4f63b"      # Male voice (Adam)
    
    print(f"Current phone ID: {current_phone_id}")
    print(f"Current assistant (Female): {current_assistant_id}")
    print(f"New assistant (Male/Adam): {new_assistant_id}")
    
    confirm = input("\nDo you want to update the phone number to use the male voice assistant? (y/N): ")
    
    if confirm.lower() == 'y':
        print(f"\n🔄 Updating phone number assignment...")
        
        result = update_phone_assistant(current_phone_id, new_assistant_id)
        
        if result:
            print(f"\n🎉 Update complete!")
            print(f"Phone number +13253081698 now uses the male voice (Adam)")
            print(f"You should now hear a male voice when you call.")
        else:
            print(f"\n❌ Update failed. Please check the error messages above.")
    else:
        print("👋 Update cancelled.")

if __name__ == "__main__":
    main()
