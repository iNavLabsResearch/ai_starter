"""
Gemini & OpenAI Client
Reference: docs/session_1/5_practical_gemini_openai.md
"""

import requests
import json
from typing import Literal
from openai import OpenAI

class GeminiClient:
    """Google Gemini API client"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        self.api_key = api_key
    
    def chat(self, prompt: str) -> str:
        """Send prompt to Gemini and get response"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            else:
                return "No response from Gemini"
        
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"


class OpenAIClient:
    """OpenAI API client using OpenAI SDK"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=api_key)
    
    def chat(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """Send prompt to OpenAI and get response"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {str(e)}"


class UnifiedAIClient:
    """Unified client for multiple AI providers"""
    
    def __init__(self, provider: Literal["openai", "gemini"], api_key: str):
        """Initialize with provider choice"""
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai":
            self.openai_client = OpenAIClient(api_key)
        elif provider == "gemini":
            self.gemini_client = GeminiClient(api_key)
    
    def chat(self, prompt: str) -> str:
        """Chat with selected AI provider"""
        if self.provider == "openai":
            return self.openai_client.chat(prompt)
        elif self.provider == "gemini":
            return self.gemini_client.chat(prompt)


class SimpleChatBot:
    """Simple chatbot using AI APIs"""
    
    def __init__(self, provider: str, api_key: str):
        """Initialize chatbot"""
        self.client = UnifiedAIClient(provider, api_key)
        self.conversation_history = []
    
    def chat(self, user_message: str) -> str:
        """Chat with user"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get AI response
        response = self.client.chat(user_message)
        
        # Add AI response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history


# Example usage
if __name__ == "__main__":
    # Test with Gemini (using provided API key)
    print("Testing Gemini API...")
    gemini_key = "AIzaSyB2yDkLyufceKxz167CE1axVmTSLDIhlRE"
    gemini = GeminiClient(gemini_key)
    
    response = gemini.chat("Explain AI in one sentence.")
    print(f"Gemini Response: {response}\n")
    
    # Test chatbot
    print("Testing SimpleChatBot with Gemini...")
    bot = SimpleChatBot("gemini", gemini_key)
    bot_response = bot.chat("What is Python?")
    print(f"Bot Response: {bot_response}\n")
    
    print("✅ All tests passed!")
