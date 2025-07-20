from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppBot:
    """WhatsApp Bot integration using Twilio API."""
    
    def __init__(self):
        """Initialize the WhatsApp bot with Twilio credentials."""
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))
        
        # Get Twilio credentials from environment
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("Twilio credentials not found in environment variables")
        
        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)
        
        logger.info("WhatsApp Bot initialized successfully")
    
    def send_message(self, to_number: str, message_body: str) -> str:
        """
        Send a message via WhatsApp.
        
        Args:
            to_number (str): Recipient's WhatsApp number (format: whatsapp:+1234567890)
            message_body (str): Message content
            
        Returns:
            str: Message SID
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_whatsapp_number,
                to=to_number
            )
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return message.sid
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise e
    
    def create_response(self, message_body: str) -> str:
        """
        Create a TwiML response for incoming messages.
        
        Args:
            message_body (str): Response message content
            
        Returns:
            str: TwiML response as string
        """
        response = MessagingResponse()
        response.message(message_body)
        return str(response)
    
    def get_message_info(self, request_form) -> dict:
        """
        Extract message information from Twilio webhook request.
        
        Args:
            request_form: Flask request.form or request.values
            
        Returns:
            dict: Message information
        """
        return {
            'from_number': request_form.get('From', ''),
            'to_number': request_form.get('To', ''),
            'message_body': request_form.get('Body', '').strip(),
            'message_sid': request_form.get('MessageSid', ''),
            'account_sid': request_form.get('AccountSid', ''),
            'from_name': request_form.get('ProfileName', 'Unknown')
        }
    
    def is_valid_webhook(self, request_form) -> bool:
        """
        Basic validation for webhook requests.
        
        Args:
            request_form: Flask request.form or request.values
            
        Returns:
            bool: True if valid webhook
        """
        required_fields = ['From', 'To', 'Body', 'MessageSid']
        return all(field in request_form for field in required_fields)
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Format phone number for WhatsApp.
        
        Args:
            phone_number (str): Phone number
            
        Returns:
            str: Formatted WhatsApp number
        """
        if not phone_number.startswith('whatsapp:'):
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            return f'whatsapp:{phone_number}'
        return phone_number
    
    def get_health_status(self) -> dict:
        """
        Get health status of the WhatsApp bot.
        
        Returns:
            dict: Health status information
        """
        try:
            # Test API connection by fetching account info
            account = self.client.api.accounts(self.account_sid).fetch()
            return {
                'status': 'healthy',
                'account_sid': self.account_sid,
                'account_status': account.status,
                'from_number': self.from_whatsapp_number
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
