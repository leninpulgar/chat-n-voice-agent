# Business AI Agent with Gemini

A Python-based AI agent powered by Google's Gemini model that can answer business inquiries based on PDF documents.

## Features

- PDF text extraction using multiple libraries (PyPDF2 and pdfplumber)
- AI-powered responses using Google Gemini
- Conversation memory to maintain context
- REST API interface
- WhatsApp integration via Twilio
- Interactive testing client
- Webhook support for real-time messaging

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access

### 2. Installation

1. Clone or download this project
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set up Twilio account and get WhatsApp credentials:
   - Create account at [Twilio](https://www.twilio.com/)
   - Get Account SID and Auth Token
   - Enable WhatsApp Sandbox
3. Update the `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```
4. Place your business PDF file in the project directory as `business_info.pdf`

### 4. Running the Application

Start the Flask server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### POST /ask
Ask a question to the AI agent
```json
{
  "question": "What are your business hours?"
}
```

### GET /health
Check the health status of the agent

### POST /clear
Clear conversation history

### GET /context
Get business summary from PDF

### POST /whatsapp
Webhook endpoint for WhatsApp messages (used by Twilio)

### POST /send-whatsapp
Send WhatsApp message manually
```json
{
  "to_number": "+1234567890",
  "message": "Hello from your business assistant!"
}
```

## Testing

### Basic Test
```bash
python test_client.py
```

### Interactive Test
```bash
python test_client.py interactive
```

### WhatsApp Testing
```bash
python test_whatsapp.py
```

## WhatsApp Setup

### 1. Set up Twilio WhatsApp Sandbox
1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to Messaging → Settings → WhatsApp Sandbox
3. Follow the instructions to join the sandbox
4. Note the sandbox number (usually +14155238886)

### 2. Configure Webhook URL
1. Start your Flask app: `python main.py`
2. In another terminal, run: `python setup_ngrok.py`
3. Copy the webhook URL provided
4. In Twilio Console, set the webhook URL to: `https://your-ngrok-url.ngrok.io/whatsapp`

### 3. Test WhatsApp Integration
1. Send a WhatsApp message to the Twilio sandbox number
2. Use the join code provided by Twilio
3. Ask questions about your business
4. The bot should respond with AI-generated answers

## Project Structure

```
project/
├── main.py                # Flask application entry point
├── gemini_agent.py        # Gemini AI agent implementation
├── pdf_processor.py       # PDF text extraction module
├── test_client.py         # Test client for the API
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (contains secret keys)
├── business_info.pdf      # Business information PDF used by the agent
├── sample_business_info.txt # Example text to create your business PDF
├── README.md              # Main project README
├── docs/                  # Documentation files
│   ├── QUICK_START_VOICE.md
│   ├── README.md            # Detailed documentation guide
│   ├── VOICE_CHAT_TUTORIAL.md
│   └── WHATSAPP_TESTING_GUIDE.md
└── venv/                  # Virtual environment (usually ignored by Git)

```

## Usage Examples

### Python Script Usage
```python
from pdf_processor import PDFProcessor
from gemini_agent import GeminiAgent

# Initialize components
pdf_processor = PDFProcessor("business_info.pdf")
business_content = pdf_processor.extract_text()

gemini_agent = GeminiAgent()
gemini_agent.set_business_context(business_content, "My Business")

# Ask questions
response = gemini_agent.generate_response("What services do you offer?")
print(response)
```

### API Usage
```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:5000/ask",
    json={"question": "What are your business hours?"}
)
print(response.json())
```

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PDF_PATH`: Path to your business PDF file (default: "business_info.pdf")
- `BUSINESS_NAME`: Name of your business (default: "Our Business")
- `PORT`: Server port (default: 5000)

## Error Handling

The application includes comprehensive error handling:
- PDF file not found
- Invalid API key
- Network errors
- Malformed requests

## Customization

### Adding New Features

1. **Custom PDF Processing**: Modify `pdf_processor.py` to handle specific PDF layouts
2. **Enhanced AI Responses**: Adjust prompts in `gemini_agent.py`
3. **New API Endpoints**: Add routes in `main.py`
4. **Database Integration**: Add database support for persistent conversation history

### Configuration Options

- Modify `generation_config` in `gemini_agent.py` for different AI behavior
- Adjust conversation memory settings in `ConversationMemory` class
- Customize Flask app settings in `main.py`

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Gemini API key is correctly set in `.env`
2. **PDF Not Loading**: Check that your PDF file exists and is readable
3. **Import Errors**: Ensure all dependencies are installed in the virtual environment
4. **Network Issues**: Check internet connection for API calls

### Debug Mode

Run with debug mode for detailed error messages:
```bash
FLASK_DEBUG=True python main.py
```

## License

This project is for educational purposes. Please ensure you comply with Google's Gemini API terms of service.

## Contributing

Feel free to submit issues and enhancement requests!
