#!/usr/bin/env python3
"""
Update Voice Assistant Script
This script updates your VAPI voice assistant with new business information
"""

import os
import json
from dotenv import load_dotenv
from vapi_integration import VAPIIntegration
from pdf_processor import PDFProcessor

def update_voice_assistant():
    """Update the voice assistant with fresh business context."""
    
    print("🔄 Updating Voice Assistant with New Business Information")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize VAPI
    try:
        vapi = VAPIIntegration()
        print("✅ VAPI connection established")
    except Exception as e:
        print(f"❌ Failed to connect to VAPI: {e}")
        return False
    
    # Load fresh business context
    print("\n📄 Loading updated business context...")
    try:
        pdf_processor = PDFProcessor("business_info.pdf")
        business_content = pdf_processor.extract_text()
        print(f"✅ Business context loaded ({len(business_content)} characters)")
    except Exception as e:
        print(f"❌ Failed to load business context: {e}")
        return False
    
    # Get existing assistants
    print("\n🔍 Finding existing assistants...")
    try:
        assistants = vapi.get_assistants()
        if not assistants:
            print("❌ No assistants found. Create one first using test_vapi_setup.py")
            return False
        
        # Find TechSolutions Pro assistant
        target_assistant = None
        for assistant in assistants:
            if "TechSolutions Pro" in assistant.get('name', ''):
                target_assistant = assistant
                break
        
        if not target_assistant:
            print("❌ TechSolutions Pro assistant not found")
            print("Available assistants:")
            for i, assistant in enumerate(assistants, 1):
                print(f"  {i}. {assistant.get('name', 'Unnamed')} (ID: {assistant.get('id')})")
            
            # Let user choose
            try:
                choice = input("\nEnter assistant number to update (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return False
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(assistants):
                    target_assistant = assistants[choice_idx]
                else:
                    print("❌ Invalid choice")
                    return False
            except ValueError:
                print("❌ Invalid input")
                return False
        
        assistant_id = target_assistant.get('id')
        assistant_name = target_assistant.get('name', 'Assistant')
        print(f"✅ Found assistant: {assistant_name} (ID: {assistant_id})")
        
    except Exception as e:
        print(f"❌ Error finding assistants: {e}")
        return False
    
    # Update the assistant
    print(f"\n🔄 Updating assistant '{assistant_name}'...")
    try:
        updated_assistant = vapi.update_assistant(
            assistant_id=assistant_id,
            business_context=business_content,
            business_name="TechSolutions Pro"
        )
        
        if updated_assistant:
            print("✅ Assistant updated successfully!")
            print(f"   Assistant ID: {assistant_id}")
            print(f"   Updated: {updated_assistant.get('updatedAt', 'N/A')}")
            
            # Get phone numbers for this assistant
            print("\n📞 Checking associated phone numbers...")
            phone_numbers = vapi.get_phone_numbers()
            if phone_numbers:
                for phone in phone_numbers:
                    if phone.get('assistantId') == assistant_id:
                        print(f"   📞 Phone: {phone.get('number')}")
                        print(f"   📞 Status: {phone.get('status', 'Unknown')}")
            
            print("\n🎉 Update Complete!")
            print("Your voice assistant now has the latest business information.")
            print("You can test it by calling the phone number.")
            
            return True
        else:
            print("❌ Failed to update assistant")
            return False
            
    except Exception as e:
        print(f"❌ Error updating assistant: {e}")
        return False

def main():
    """Main function."""
    
    print("Voice Assistant Update Tool")
    print("This tool updates your VAPI voice assistant with fresh business information.")
    print()
    
    # Check if PDF file exists
    if not os.path.exists("business_info.pdf"):
        print("❌ business_info.pdf not found in current directory")
        print("Please ensure your business PDF file is named 'business_info.pdf' and is in the project directory.")
        return
    
    # Confirm update
    confirm = input("Do you want to update your voice assistant with the latest business information? (y/N): ")
    if confirm.lower() not in ['y', 'yes']:
        print("Update cancelled.")
        return
    
    # Run the update
    success = update_voice_assistant()
    
    if success:
        print("\n✅ Voice assistant updated successfully!")
        print("💡 Pro tip: Test the updated assistant by making a call to verify the changes.")
    else:
        print("\n❌ Update failed. Please check the errors above.")

if __name__ == "__main__":
    main()
