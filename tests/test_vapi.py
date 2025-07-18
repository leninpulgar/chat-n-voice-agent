# Test VAPI Integration
from vapi_integration import VAPIIntegration

# Initialize VAPI
vapi = VAPIIntegration()

# Load business info from PDF
business_context = """Your sample business information goes here..."""

# Create a Voice Assistant
assistant_info = vapi.create_assistant(business_context)

if assistant_info:
    print("Assistant Created:", assistant_info)
    
    # Create a Phone Number
    phone_info = vapi.create_phone_number(assistant_info.get('id'))
    
    if phone_info:
        print("Phone Number Created:", phone_info)
else:
    print("Failed to create assistant.")

# Health Check
health = vapi.health_check()
print("VAPI Health:", health)
