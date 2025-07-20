import os
import json
import requests
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VAPIIntegration:
    """VAPI integration for voice chat functionality."""
    
    def __init__(self):
        """Initialize VAPI integration."""
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))
        
        self.api_key = os.getenv('VAPI_API_KEY')
        self.base_url = "https://api.vapi.ai"
        
        if not self.api_key:
            raise ValueError("VAPI_API_KEY not found in environment variables")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info("VAPI integration initialized")
    
    def _get_voice_config(self) -> Dict[str, Any]:
        """
        Get voice configuration from environment variables or use defaults.
        
        Returns:
            Dict[str, Any]: Voice configuration
        """
        provider = os.getenv('VAPI_VOICE_PROVIDER', '11labs').lower()
        
        if provider == '11labs' or provider == 'elevenlabs':
            return {
                "provider": "11labs",
                "voiceId": os.getenv('VAPI_VOICE_ID', '21m00Tcm4TlvDq8ikWAM'),  # Default: Rachel
                "stability": float(os.getenv('VAPI_VOICE_STABILITY', '0.5')),
                "similarityBoost": float(os.getenv('VAPI_VOICE_SIMILARITY_BOOST', '0.8'))
            }
        elif provider == 'openai':
            return {
                "provider": "openai",
                "voice": os.getenv('VAPI_VOICE_ID', 'alloy')  # Options: alloy, echo, fable, onyx, nova, shimmer
            }
        elif provider == 'azure':
            return {
                "provider": "azure",
                "voice": os.getenv('VAPI_VOICE_ID', 'en-US-JennyNeural')
            }
        elif provider == 'playht':
            return {
                "provider": "playht",
                "voice": os.getenv('VAPI_VOICE_ID', 'jennifer')
            }
        else:
            # Fallback to 11labs default
            return {
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM",
                "stability": 0.5,
                "similarityBoost": 0.8
            }

    def create_assistant(self, business_context: str, business_name: str = "Business Assistant") -> Dict[str, Any]:
        """
        Create a VAPI assistant with business context.
        
        Args:
            business_context (str): Business information from PDF
            business_name (str): Name of the business
            
        Returns:
            Dict[str, Any]: Assistant configuration
        """
        
        # Create system prompt with business context
        system_prompt = f"""You are a helpful business assistant for {business_name}.
        
Your role is to answer customer inquiries accurately and professionally based on the business information provided.

IMPORTANT GUIDELINES:
1. Always base your answers on the business information provided
2. If you don't know something or it's not in the business information, say so honestly
3. Be professional, friendly, and helpful
4. Keep responses concise but complete
5. Speak naturally as if you're having a phone conversation
6. If asked about services, prices, or policies not mentioned in the business info, direct them to contact the business directly

BUSINESS INFORMATION:
{business_context}

Please provide helpful responses to customer inquiries about the business."""

        assistant_config = {
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]
            },
            "voice": self._get_voice_config(),
            "firstMessage": f"Hello! I'm your {business_name} assistant. How can I help you today?",
            "recordingEnabled": False,
            "silenceTimeoutSeconds": 30,
            "maxDurationSeconds": 600,  # 10 minutes max call duration
            "backgroundSound": "office",
            "backchannelingEnabled": True,
            "name": f"{business_name} Voice Assistant"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/assistant",
                headers=self.headers,
                json=assistant_config
            )
            
            if response.status_code == 201:
                assistant_data = response.json()
                logger.info(f"Assistant created successfully: {assistant_data.get('id')}")
                return assistant_data
            else:
                logger.error(f"Failed to create assistant: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating assistant: {e}")
            return None
    
    def create_phone_number(self, assistant_id: str, phone_number: str = None) -> Dict[str, Any]:
        """
        Create a phone number for the voice assistant.
        
        Args:
            assistant_id (str): ID of the created assistant
            phone_number (str, optional): Specific phone number to use (E.164 format)
            
        Returns:
            Dict[str, Any]: Phone number configuration
        """
        
        # Check if Twilio credentials are available
        twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not twilio_sid or not twilio_token:
            logger.warning("Twilio credentials not found. Cannot create phone number.")
            return None
        
        # If no phone number provided, try to purchase one from Twilio
        if not phone_number:
            phone_number = self._purchase_twilio_number(twilio_sid, twilio_token)
            if not phone_number:
                logger.error("Failed to purchase phone number from Twilio")
                return None
        
        # Create phone number configuration
        phone_config = {
            "assistantId": assistant_id,
            "provider": "twilio",
            "twilioAccountSid": twilio_sid,
            "twilioAuthToken": twilio_token,
            "name": "Business Voice Assistant",
            "number": phone_number
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/phone-number",
                headers=self.headers,
                json=phone_config
            )
            
            if response.status_code == 201:
                phone_data = response.json()
                logger.info(f"Phone number created: {phone_data.get('number')}")
                return phone_data
            else:
                logger.error(f"Failed to create phone number: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating phone number: {e}")
            return None
    
    def _purchase_twilio_number(self, account_sid: str, auth_token: str) -> str:
        """
        Purchase a phone number from Twilio.
        
        Args:
            account_sid (str): Twilio account SID
            auth_token (str): Twilio auth token
            
        Returns:
            str: Purchased phone number in E.164 format
        """
        try:
            # First, search for available phone numbers
            search_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/AvailablePhoneNumbers/US/Local.json"
            auth = (account_sid, auth_token)
            
            search_response = requests.get(search_url, auth=auth)
            
            if search_response.status_code == 200:
                available_numbers = search_response.json().get('available_phone_numbers', [])
                
                if available_numbers:
                    # Get the first available number
                    selected_number = available_numbers[0]['phone_number']
                    
                    # Purchase the number
                    purchase_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/IncomingPhoneNumbers.json"
                    purchase_data = {
                        'PhoneNumber': selected_number,
                        'FriendlyName': 'VAPI Business Assistant'
                    }
                    
                    purchase_response = requests.post(purchase_url, data=purchase_data, auth=auth)
                    
                    if purchase_response.status_code == 201:
                        logger.info(f"Successfully purchased phone number: {selected_number}")
                        return selected_number
                    else:
                        logger.error(f"Failed to purchase phone number: {purchase_response.status_code} - {purchase_response.text}")
                        return None
                else:
                    logger.error("No available phone numbers found")
                    return None
            else:
                logger.error(f"Failed to search for available numbers: {search_response.status_code} - {search_response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error purchasing Twilio number: {e}")
            return None
    
    def get_assistants(self) -> Dict[str, Any]:
        """Get all assistants."""
        try:
            response = requests.get(
                f"{self.base_url}/assistant",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get assistants: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting assistants: {e}")
            return None
    
    def get_phone_numbers(self) -> Dict[str, Any]:
        """Get all phone numbers."""
        try:
            response = requests.get(
                f"{self.base_url}/phone-number",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get phone numbers: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting phone numbers: {e}")
            return None
    
    def update_assistant(self, assistant_id: str, business_context: str, business_name: str = "Business Assistant") -> Dict[str, Any]:
        """
        Update an existing assistant with new business context.
        
        Args:
            assistant_id (str): ID of the assistant to update
            business_context (str): Updated business information
            business_name (str): Name of the business
            
        Returns:
            Dict[str, Any]: Updated assistant configuration
        """
        
        system_prompt = f"""You are a helpful business assistant for {business_name}.
        
Your role is to answer customer inquiries accurately and professionally based on the business information provided.

IMPORTANT GUIDELINES:
1. Always base your answers on the business information provided
2. If you don't know something or it's not in the business information, say so honestly
3. Be professional, friendly, and helpful
4. Keep responses concise but complete
5. Speak naturally as if you're having a phone conversation
6. If asked about services, prices, or policies not mentioned in the business info, direct them to contact the business directly

BUSINESS INFORMATION:
{business_context}

Please provide helpful responses to customer inquiries about the business."""

        update_config = {
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]
            },
            "firstMessage": f"Hello! I'm your {business_name} assistant. How can I help you today?"
        }
        
        try:
            response = requests.patch(
                f"{self.base_url}/assistant/{assistant_id}",
                headers=self.headers,
                json=update_config
            )
            
            if response.status_code == 200:
                assistant_data = response.json()
                logger.info(f"Assistant updated successfully: {assistant_id}")
                return assistant_data
            else:
                logger.error(f"Failed to update assistant: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error updating assistant: {e}")
            return None
    
    def delete_assistant(self, assistant_id: str) -> bool:
        """
        Delete an assistant.
        
        Args:
            assistant_id (str): ID of the assistant to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.delete(
                f"{self.base_url}/assistant/{assistant_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                logger.info(f"Assistant deleted successfully: {assistant_id}")
                return True
            else:
                logger.error(f"Failed to delete assistant: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting assistant: {e}")
            return False
    
    def get_call_logs(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get call logs.
        
        Args:
            limit (int): Number of call logs to retrieve
            
        Returns:
            Dict[str, Any]: Call logs data
        """
        try:
            response = requests.get(
                f"{self.base_url}/call?limit={limit}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get call logs: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting call logs: {e}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check VAPI service health.
        
        Returns:
            Dict[str, Any]: Health status
        """
        try:
            response = requests.get(
                f"{self.base_url}/assistant",
                headers=self.headers
            )
            
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "api_key_set": bool(self.api_key),
                "response_code": response.status_code
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "api_key_set": bool(self.api_key)
            }
