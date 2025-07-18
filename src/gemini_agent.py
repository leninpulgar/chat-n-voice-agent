import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import json

class ConversationMemory:
    """Simple conversation memory to maintain context."""
    
    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
    
    def add_exchange(self, question: str, answer: str):
        """Add a question-answer pair to history."""
        self.history.append({
            'question': question,
            'answer': answer,
            'timestamp': None  # You can add timestamp if needed
        })
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self, limit: int = 5) -> List[Dict]:
        """Get recent conversation context."""
        return self.history[-limit:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.history = []

class GeminiAgent:
    """AI Agent powered by Google's Gemini model for business inquiries."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the Gemini Agent.
        
        Args:
            model_name (str): Name of the Gemini model to use
        """
        # Load environment variables
        load_dotenv()
        
        # Configure Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("Please set your GEMINI_API_KEY in the .env file")
        
        genai.configure(api_key=api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(model_name)
        
        # Business context and memory
        self.business_context = ""
        self.memory = ConversationMemory()
        
        # Generation config for better responses
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    
    def set_business_context(self, pdf_content: str, business_name: str = "Our Business"):
        """
        Set the business context from PDF content.
        
        Args:
            pdf_content (str): Text content from business PDF
            business_name (str): Name of the business
        """
        self.business_context = pdf_content
        self.business_name = business_name
        print(f"Business context loaded. Content length: {len(pdf_content)} characters")
    
    def _build_prompt(self, user_query: str, include_history: bool = True) -> str:
        """
        Build the prompt for Gemini including context and history.
        
        Args:
            user_query (str): User's question
            include_history (bool): Whether to include conversation history
            
        Returns:
            str: Complete prompt for Gemini
        """
        # Base system prompt
        system_prompt = f"""You are a helpful business assistant AI for {getattr(self, 'business_name', 'this business')}. 
Your role is to answer customer inquiries accurately and helpfully based on the business information provided.

IMPORTANT GUIDELINES:
1. Always base your answers on the business information provided
2. If you don't know something or it's not in the business information, say so honestly
3. Be professional, friendly, and helpful
4. Keep responses concise but complete
5. If asked about services, prices, or policies not mentioned in the business info, direct them to contact the business directly

BUSINESS INFORMATION:
{self.business_context}

"""
        
        # Add conversation history if requested
        if include_history and self.memory.history:
            system_prompt += "RECENT CONVERSATION HISTORY:\n"
            for exchange in self.memory.get_context():
                system_prompt += f"Q: {exchange['question']}\nA: {exchange['answer']}\n\n"
        
        # Add current user query
        system_prompt += f"CURRENT CUSTOMER QUESTION: {user_query}\n\n"
        system_prompt += "Please provide a helpful response based on the business information:"
        
        return system_prompt
    
    def generate_response(self, user_query: str, include_history: bool = True) -> str:
        """
        Generate a response to user query using Gemini.
        
        Args:
            user_query (str): User's question
            include_history (bool): Whether to include conversation history
            
        Returns:
            str: Generated response
        """
        try:
            if not self.business_context:
                return "I'm sorry, but I don't have access to business information yet. Please contact the business directly for assistance."
            
            # Build the prompt
            prompt = self._build_prompt(user_query, include_history)
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Extract response text
            response_text = response.text
            
            # Add to memory
            self.memory.add_exchange(user_query, response_text)
            
            return response_text
            
        except Exception as e:
            error_msg = f"I apologize, but I'm having trouble processing your request right now. Please try again later or contact us directly."
            print(f"Error generating response: {e}")
            return error_msg
    
    def get_business_summary(self) -> str:
        """
        Generate a summary of the business based on the PDF content.
        
        Returns:
            str: Business summary
        """
        if not self.business_context:
            return "No business information available."
        
        summary_prompt = f"""Based on the following business information, provide a brief summary covering:
1. What the business does
2. Key services or products
3. Contact information if available
4. Any important policies or information

Business Information:
{self.business_context}

Please provide a concise summary:"""
        
        try:
            response = self.model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate summary: {e}"
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.memory.clear_history()
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history."""
        return self.memory.history
    
    def health_check(self) -> Dict:
        """
        Check the health status of the agent.
        
        Returns:
            dict: Health status information
        """
        return {
            "status": "healthy" if self.business_context else "no_context",
            "business_context_loaded": bool(self.business_context),
            "context_length": len(self.business_context),
            "conversation_history_length": len(self.memory.history),
            "model_name": self.model.model_name if hasattr(self.model, 'model_name') else "gemini-pro"
        }
