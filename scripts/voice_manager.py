#!/usr/bin/env python3
"""
VAPI Voice Manager
Comprehensive tool for managing voice assistants and phone number assignments
"""

import os
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vapi_integration import VAPIIntegration
from pdf_processor import PDFProcessor
import json

# Voice options with different languages
VOICE_OPTIONS = {
    "1": {
        "name": "Rachel (English, Female, Professional)",
        "provider": "11labs",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "stability": "0.5",
        "similarity_boost": "0.8",
        "language": "en"
    },
    "2": {
        "name": "Adam (English, Male, Deep)",
        "provider": "11labs", 
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "stability": "0.6",
        "similarity_boost": "0.8",
        "language": "en"
    },
    "3": {
        "name": "Bella (English, Female, Friendly)",
        "provider": "11labs",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "stability": "0.4",
        "similarity_boost": "0.9",
        "language": "en"
    },
    "4": {
        "name": "Antoni (English, Male, Mature)",
        "provider": "11labs",
        "voice_id": "ErXwobaYiN019PkySvjV",
        "stability": "0.7",
        "similarity_boost": "0.8",
        "language": "en"
    },
    "5": {
        "name": "Domi (English, Female, Strong)",
        "provider": "11labs",
        "voice_id": "AZnzlk1XvdvUeBnXmlld",
        "stability": "0.6",
        "similarity_boost": "0.8",
        "language": "en"
    },
    "6": {
        "name": "OpenAI Alloy (English, Neutral)",
        "provider": "openai",
        "voice_id": "alloy",
        "language": "en"
    },
    "7": {
        "name": "OpenAI Nova (English, Female)",
        "provider": "openai",
        "voice_id": "nova",
        "language": "en"
    },
    "8": {
        "name": "OpenAI Alloy (Spanish Mode)",
        "provider": "openai",
        "voice_id": "alloy",
        "language": "es"
    },
    "9": {
        "name": "OpenAI Nova (Spanish Mode)",
        "provider": "openai",
        "voice_id": "nova",
        "language": "es"
    },
    "10": {
        "name": "OpenAI Echo (Chinese Mode)",
        "provider": "openai",
        "voice_id": "echo",
        "language": "zh"
    }
}

class VoiceManager:
    def __init__(self):
        self.vapi = VAPIIntegration()
        self.current_phone_id = "08683264-de30-47d3-9c52-1af12d9e1dc7"
    
    def get_current_assistant_id(self):
        """Get the current assistant ID for the phone number."""
        try:
            phone_numbers = self.vapi.get_phone_numbers()
            for phone in phone_numbers:
                if phone['id'] == self.current_phone_id:
                    return phone['assistantId']
            return None
        except Exception as e:
            print(f"Error getting current assistant: {e}")
            return None
    
    def update_assistant_voice(self, assistant_id, voice_config, language="en"):
        """Update an existing assistant's voice configuration."""
        try:
            # Get assistant details first
            response = requests.get(
                f"{self.vapi.base_url}/assistant/{assistant_id}",
                headers=self.vapi.headers
            )
            
            if response.status_code != 200:
                print(f"Failed to get assistant details: {response.status_code}")
                return None
            
            assistant = response.json()
            
            # Update voice configuration
            assistant['voice'] = voice_config
            
            # Update the assistant
            update_response = requests.patch(
                f"{self.vapi.base_url}/assistant/{assistant_id}",
                headers=self.vapi.headers,
                json={"voice": voice_config}
            )
            
            if update_response.status_code == 200:
                return update_response.json()
            else:
                print(f"Failed to update assistant voice: {update_response.status_code} - {update_response.text}")
                return None
                
        except Exception as e:
            print(f"Error updating assistant voice: {e}")
            return None
    
    def create_new_assistant_with_voice(self, voice_config, language="en"):
        """Create a new assistant with specified voice and language."""
        try:
            # Load business context
            pdf_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'business_info.pdf')
            pdf_processor = PDFProcessor(pdf_path)
            business_content = pdf_processor.extract_text()
            
            # Create language-specific business name
            if language == "es":
                business_name = "TechSolutions Pro (Español)"
            elif language == "zh":
                business_name = "TechSolutions Pro (中文)"
            else:
                business_name = "TechSolutions Pro"
            
            # Create system prompt based on language
            system_prompt = self._create_multilingual_prompt(business_content, business_name, language)
            
            # Create assistant config
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
                "voice": voice_config,
                "firstMessage": self._get_first_message(business_name, language),
                "recordingEnabled": False,
                "silenceTimeoutSeconds": 30,
                "maxDurationSeconds": 600,
                "backgroundSound": "office",
                "backchannelingEnabled": True,
                "name": f"{business_name} Assistant"
            }
            
            # Add transcriber for non-English languages
            if language != "en":
                assistant_config["transcriber"] = self._get_transcriber_config(language)
            
            response = requests.post(
                f"{self.vapi.base_url}/assistant",
                headers=self.vapi.headers,
                json=assistant_config
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Failed to create assistant: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating assistant: {e}")
            return None
    
    def _create_multilingual_prompt(self, business_content, business_name, language):
        """Create system prompt for different languages."""
        
        if language == "es":
            return f"""Eres un asistente empresarial útil para {business_name}.

Tu función es responder consultas de clientes de manera precisa y profesional basándote en la información empresarial proporcionada.

PAUTAS IMPORTANTES:
1. Siempre basa tus respuestas en la información empresarial proporcionada
2. Si no sabes algo o no está en la información empresarial, dilo honestamente
3. Sé profesional, amigable y útil
4. Mantén las respuestas concisas pero completas
5. Habla naturalmente como si estuvieras teniendo una conversación telefónica
6. Si te preguntan sobre servicios, precios o políticas no mencionadas en la información empresarial, dirige al cliente a contactar directamente con la empresa

INFORMACIÓN EMPRESARIAL:
{business_content}

Por favor, proporciona respuestas útiles a las consultas de clientes sobre la empresa."""

        elif language == "zh":
            return f"""您是{business_name}的有用商务助理。

您的职责是根据提供的商务信息准确、专业地回答客户咨询。

重要准则：
1. 始终根据提供的商务信息回答
2. 如果不知道某事或商务信息中没有，请诚实说明
3. 保持专业、友好和有帮助的态度
4. 保持回答简洁但完整
5. 像电话交谈一样自然地说话
6. 如果询问商务信息中未提及的服务、价格或政策，请引导客户直接联系企业

商务信息：
{business_content}

请为客户关于企业的咨询提供有用的回答。"""

        else:  # English
            return f"""You are a helpful business assistant for {business_name}.

Your role is to answer customer inquiries accurately and professionally based on the business information provided.

IMPORTANT GUIDELINES:
1. Always base your answers on the business information provided
2. If you don't know something or it's not in the business information, say so honestly
3. Be professional, friendly, and helpful
4. Keep responses concise but complete
5. Speak naturally as if you're having a phone conversation
6. If asked about services, prices, or policies not mentioned in the business info, direct them to contact the business directly

BUSINESS INFORMATION:
{business_content}

Please provide helpful responses to customer inquiries about the business."""

    def _get_first_message(self, business_name, language):
        """Get first message in appropriate language."""
        if language == "es":
            return f"¡Hola! Soy tu asistente de {business_name}. ¿Cómo puedo ayudarte hoy?"
        elif language == "zh":
            return f"您好！我是您的{business_name}助理。今天我可以为您做些什么？"
        else:
            return f"Hello! I'm your {business_name} assistant. How can I help you today?"

    def _get_transcriber_config(self, language):
        """Get transcriber configuration for different languages."""
        language_codes = {
            "es": "es",
            "zh": "zh",
            "en": "en"
        }
        
        return {
            "model": "nova-2",
            "language": language_codes.get(language, "en"),
            "provider": "deepgram"
        }

    def _get_voice_config(self, choice):
        """Get voice configuration from choice."""
        if choice not in VOICE_OPTIONS:
            return None
        
        config = VOICE_OPTIONS[choice]
        
        if config['provider'] == '11labs':
            return {
                "provider": "11labs",
                "voiceId": config['voice_id'],
                "stability": float(config['stability']),
                "similarityBoost": float(config['similarity_boost'])
            }
        elif config['provider'] == 'openai':
            return {
                "provider": "openai",
                "voiceId": config['voice_id']
            }
        elif config['provider'] == 'azure':
            return {
                "provider": "azure",
                "voice": config['voice_id']
            }
        
        return None

    def update_phone_assistant(self, new_assistant_id):
        """Update phone number to use a different assistant."""
        try:
            update_data = {"assistantId": new_assistant_id}
            
            response = requests.patch(
                f"{self.vapi.base_url}/phone-number/{self.current_phone_id}",
                headers=self.vapi.headers,
                json=update_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to update phone number: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error updating phone number: {e}")
            return None

def main():
    print("🎤 VAPI Voice & Language Manager")
    print("=" * 50)
    
    # Show available voices
    print("\nAvailable Voice & Language Options:")
    for key, config in VOICE_OPTIONS.items():
        print(f"{key:2}. {config['name']}")
    
    print("\nWhat would you like to do?")
    print("A. Change voice (update current assistant)")
    print("B. Create new assistant with different voice/language")
    print("C. Just show voice configuration")
    print("D. Exit")
    
    choice = input("\nEnter your choice (A/B/C/D): ").upper()
    
    if choice == 'A':
        # Update current assistant voice
        voice_choice = input(f"\nChoose a voice (1-{len(VOICE_OPTIONS)}): ")
        
        if voice_choice in VOICE_OPTIONS:
            manager = VoiceManager()
            current_assistant_id = manager.get_current_assistant_id()
            
            if not current_assistant_id:
                print("❌ Could not find current assistant ID")
                return
            
            voice_config = manager._get_voice_config(voice_choice)
            language = VOICE_OPTIONS[voice_choice]['language']
            
            print(f"\n🔄 Updating current assistant voice to: {VOICE_OPTIONS[voice_choice]['name']}")
            
            result = manager.update_assistant_voice(current_assistant_id, voice_config, language)
            
            if result:
                print(f"✅ Voice updated successfully!")
                print(f"Your phone number now uses: {VOICE_OPTIONS[voice_choice]['name']}")
            else:
                print(f"❌ Failed to update voice")
    
    elif choice == 'B':
        # Create new assistant
        voice_choice = input(f"\nChoose a voice (1-{len(VOICE_OPTIONS)}): ")
        
        if voice_choice in VOICE_OPTIONS:
            manager = VoiceManager()
            voice_config = manager._get_voice_config(voice_choice)
            language = VOICE_OPTIONS[voice_choice]['language']
            
            print(f"\n🔄 Creating new assistant with: {VOICE_OPTIONS[voice_choice]['name']}")
            
            assistant = manager.create_new_assistant_with_voice(voice_config, language)
            
            if assistant:
                print(f"✅ New assistant created: {assistant['id']}")
                
                update_phone = input("\nUpdate phone number to use this new assistant? (y/N): ")
                if update_phone.lower() == 'y':
                    phone_result = manager.update_phone_assistant(assistant['id'])
                    if phone_result:
                        print(f"✅ Phone number updated!")
                        print(f"Your phone number now uses: {VOICE_OPTIONS[voice_choice]['name']}")
            else:
                print(f"❌ Failed to create assistant")
    
    elif choice == 'C':
        # Show configuration
        voice_choice = input(f"\nChoose a voice to view (1-{len(VOICE_OPTIONS)}): ")
        
        if voice_choice in VOICE_OPTIONS:
            config = VOICE_OPTIONS[voice_choice]
            print(f"\n📋 Configuration for: {config['name']}")
            print("-" * 40)
            print(f"Provider: {config['provider']}")
            print(f"Voice ID: {config['voice_id']}")
            print(f"Language: {config['language']}")
            
            if config['provider'] == '11labs':
                print(f"Stability: {config['stability']}")
                print(f"Similarity Boost: {config['similarity_boost']}")
    
    elif choice == 'D':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
