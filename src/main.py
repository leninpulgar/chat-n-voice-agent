from pdf_processor import PDFProcessor
from gemini_agent import GeminiAgent
from whatsapp_integration import WhatsAppBot
from vapi_integration import VAPIIntegration
from flask import Flask, request, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Environment settings
PDF_PATH = os.getenv("PDF_PATH", "business_info.pdf")  # Default PDF file
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "TechSolutions Pro")

# Initialize components
try:
    pdf_processor = PDFProcessor(PDF_PATH)
    business_content = pdf_processor.extract_text()
    gemini_agent = GeminiAgent()
    gemini_agent.set_business_context(business_content, BUSINESS_NAME)
    whatsapp_bot = WhatsAppBot()
    
    # Initialize VAPI for voice assistant
    try:
        vapi_integration = VAPIIntegration()
        logger.info("VAPI integration initialized")
    except Exception as vapi_error:
        logger.warning(f"VAPI integration failed: {vapi_error}")
        vapi_integration = None
    
    logger.info("All components initialized successfully")
except FileNotFoundError as e:
    logger.error(f"Error loading PDF file: {e}")
    gemini_agent = GeminiAgent()  # Initialize without context
    whatsapp_bot = WhatsAppBot()
    vapi_integration = None
except Exception as e:
    logger.error(f"Error initializing components: {e}")
    gemini_agent = GeminiAgent()
    whatsapp_bot = None
    vapi_integration = None

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Webhook endpoint for WhatsApp messages."""
    try:
        # Get message information
        message_info = whatsapp_bot.get_message_info(request.values)
        
        # Validate webhook
        if not whatsapp_bot.is_valid_webhook(request.values):
            return "Invalid webhook", 400
        
        incoming_message = message_info['message_body']
        from_number = message_info['from_number']
        
        logger.info(f"Received message from {from_number}: {incoming_message}")
        
        if incoming_message:
            # Generate AI response
            ai_response = gemini_agent.generate_response(incoming_message)
            
            # Create TwiML response
            twiml_response = whatsapp_bot.create_response(ai_response)
            
            logger.info(f"Sent response: {ai_response}")
            
            return twiml_response, 200, {'Content-Type': 'text/xml'}
        else:
            return whatsapp_bot.create_response("Hello! How can I help you today?"), 200, {'Content-Type': 'text/xml'}
            
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}")
        error_response = whatsapp_bot.create_response("I'm sorry, I'm having trouble processing your message right now. Please try again later.")
        return error_response, 200, {'Content-Type': 'text/xml'}

@app.route('/ask', methods=['POST'])
def ask_question():
    """Endpoint to handle user questions."""
    try:
        user_question = request.json.get('question')
        response = gemini_agent.generate_response(user_question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e), 'message': "An error occurred handling the request."}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint for health checks."""
    gemini_health = gemini_agent.health_check()
    whatsapp_health = whatsapp_bot.get_health_status() if whatsapp_bot else {'status': 'unavailable'}
    vapi_health = vapi_integration.health_check() if vapi_integration else {'status': 'unavailable'}
    
    return jsonify({
        'gemini': gemini_health,
        'whatsapp': whatsapp_health,
        'vapi': vapi_health
    })

@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Endpoint to clear conversation history."""
    gemini_agent.clear_conversation()
    return jsonify({'message': 'Conversation history cleared.'})

@app.route('/context', methods=['GET'])
def get_context():
    """Endpoint to retrieve business context summary."""
    summary = gemini_agent.get_business_summary()
    return jsonify({'summary': summary})

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp_message():
    """Endpoint to send WhatsApp messages manually."""
    try:
        data = request.json
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({'error': 'Missing to_number or message'}), 400
        
        # Format phone number
        formatted_number = whatsapp_bot.format_phone_number(to_number)
        
        # Send message
        message_sid = whatsapp_bot.send_message(formatted_number, message)
        
        return jsonify({
            'message_sid': message_sid,
            'status': 'sent',
            'to': formatted_number
        })
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
