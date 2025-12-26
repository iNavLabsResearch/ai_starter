"""
OOP as Agent Identities
Reference: docs/session_1/3_advanced_python_oop.md
"""

class AIAgent:
    """A simple AI agent class"""
    
    def __init__(self, name, model="gpt-4"):
        """Initialize the agent"""
        self.name = name
        self.model = model
        self.conversation_history = []
    
    def respond(self, user_message):
        """Agent responds to user"""
        response = f"{self.name} says: I understand '{user_message}'"
        self.conversation_history.append({
            "user": user_message,
            "agent": response
        })
        return response
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history


class LegalAgent(AIAgent):
    """Specialized agent for legal advice"""
    
    def __init__(self, name):
        super().__init__(name)
        self.domain = "Legal"
        self.restricted_topics = ["illegal activities"]
    
    def respond(self, query):
        """Legal-specific response with safety checks"""
        if any(topic in query.lower() for topic in self.restricted_topics):
            return f"{self.name}: I cannot assist with illegal queries."
        return f"{self.name}: I can help with legal questions about: {query}"


# Example usage
if __name__ == "__main__":
    # Basic agent
    agent = AIAgent("ChatBot", "gpt-4")
    response = agent.respond("Hello!")
    print(response)
    
    # Legal agent
    legal_bot = LegalAgent("LegalAssistant")
    response1 = legal_bot.respond("How to file taxes?")
    print(response1)
    
    response2 = legal_bot.respond("How to hack a system?")
    print(response2)

