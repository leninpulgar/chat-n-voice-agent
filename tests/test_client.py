import requests
import json

class BusinessAgentClient:
    """Client to test the Business AI Agent API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def ask_question(self, question: str) -> dict:
        """Ask a question to the AI agent."""
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self) -> dict:
        """Check the health of the AI agent."""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def clear_conversation(self) -> dict:
        """Clear the conversation history."""
        try:
            response = requests.post(f"{self.base_url}/clear")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_business_summary(self) -> dict:
        """Get the business summary."""
        try:
            response = requests.get(f"{self.base_url}/context")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def test_basic_functionality():
    """Test basic functionality of the AI agent."""
    client = BusinessAgentClient()
    
    print("=== Business AI Agent Test ===\n")
    
    # Test health check
    print("1. Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    print()
    
    # Test business summary
    print("2. Business Summary:")
    summary = client.get_business_summary()
    print(json.dumps(summary, indent=2))
    print()
    
    # Test questions
    test_questions = [
        "What services do you offer?",
        "What are your business hours?",
        "How can I contact you?",
        "What is your return policy?",
        "Do you offer customer support?"
    ]
    
    print("3. Testing Questions:")
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Q: {question}")
        response = client.ask_question(question)
        if 'response' in response:
            print(f"   A: {response['response']}")
        else:
            print(f"   Error: {response}")
    
    # Test conversation clearing
    print("\n4. Clearing Conversation:")
    clear_result = client.clear_conversation()
    print(json.dumps(clear_result, indent=2))

def interactive_test():
    """Interactive testing mode."""
    client = BusinessAgentClient()
    
    print("=== Interactive Business AI Agent Test ===")
    print("Type 'quit' to exit, 'health' for health check, 'clear' to clear conversation")
    print("Type 'summary' to get business summary")
    print()
    
    while True:
        question = input("Ask a question: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'health':
            health = client.health_check()
            print(json.dumps(health, indent=2))
        elif question.lower() == 'clear':
            clear_result = client.clear_conversation()
            print(json.dumps(clear_result, indent=2))
        elif question.lower() == 'summary':
            summary = client.get_business_summary()
            print(json.dumps(summary, indent=2))
        elif question:
            response = client.ask_question(question)
            if 'response' in response:
                print(f"Response: {response['response']}")
            else:
                print(f"Error: {response}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        test_basic_functionality()
