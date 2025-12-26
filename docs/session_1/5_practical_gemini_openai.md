# 5. Practical: Gemini & OpenAI Integration

![InavLabs Logo](../../public/images/inavlabs.png)

## 🎯 Learning Objectives

By the end of this section, you'll:
- Integrate with Google Gemini API
- Integrate with OpenAI API
- Build working chat applications
- Handle API responses and errors

---

## 🤖 Part 1: Google Gemini API

### Setting Up Gemini

```python
import requests
import json

class GeminiClient:
    """Google Gemini API client"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def chat(self, prompt: str) -> str:
        """Send prompt to Gemini and get response"""
        url = f"{self.base_url}?key={self.api_key}"
        
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

# Usage
gemini = GeminiClient("YOUR_GEMINI_API_KEY")
response = gemini.chat("Explain AI in simple terms")
print(response)
```

---

### Gemini with Streaming

```python
class GeminiStreamingClient:
    """Gemini client with streaming support"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:streamGenerateContent"
    
    def stream_chat(self, prompt: str):
        """Stream response from Gemini"""
        url = f"{self.base_url}?key={self.api_key}"
        
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
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                try:
                    data = json.loads(decoded)
                    if 'candidates' in data:
                        for candidate in data['candidates']:
                            if 'content' in candidate:
                                text = candidate['content']['parts'][0].get('text', '')
                                if text:
                                    print(text, end='', flush=True)
                except json.JSONDecodeError:
                    pass

# Usage
gemini = GeminiStreamingClient("YOUR_GEMINI_API_KEY")
print("Gemini says: ", end='')
gemini.stream_chat("Tell me a short story about AI")
print()  # New line at end
```

---

## 🎨 Part 2: OpenAI API

### Basic OpenAI Integration

```python
class OpenAIClient:
    """OpenAI API client"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client"""
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """Send prompt to OpenAI and get response"""
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

# Usage
openai = OpenAIClient("YOUR_OPENAI_API_KEY")
response = openai.chat("What is machine learning?")
print(response)
```

---

### OpenAI with Streaming

```python
class OpenAIStreamingClient:
    """OpenAI client with streaming"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def stream_chat(self, prompt: str, model: str = "gpt-3.5-turbo"):
        """Stream response from OpenAI"""
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "stream": True  # Enable streaming
        }
        
        response = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    json_str = decoded[6:]  # Remove 'data: ' prefix
                    if json_str == '[DONE]':
                        break
                    
                    try:
                        data = json.loads(json_str)
                        if 'choices' in data:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                print(content, end='', flush=True)
                    except json.JSONDecodeError:
                        pass

# Usage
openai = OpenAIStreamingClient("YOUR_OPENAI_API_KEY")
print("OpenAI says: ", end='')
openai.stream_chat("Explain quantum computing simply")
print()
```

---

## 🎯 Part 3: Unified AI Client

### Multi-Provider AI Client

```python
from typing import Literal

class UnifiedAIClient:
    """Unified client for multiple AI providers"""
    
    def __init__(self, provider: Literal["openai", "gemini"], api_key: str):
        """Initialize with provider choice"""
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        elif provider == "gemini":
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            self.api_key = api_key
    
    def chat(self, prompt: str, stream: bool = False) -> str:
        """Chat with selected AI provider"""
        if self.provider == "openai":
            return self._openai_chat(prompt, stream)
        elif self.provider == "gemini":
            return self._gemini_chat(prompt, stream)
    
    def _openai_chat(self, prompt: str, stream: bool) -> str:
        """OpenAI chat implementation"""
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream
        }
        
        response = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            stream=stream
        )
        response.raise_for_status()
        
        if stream:
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data: '):
                        json_str = decoded[6:]
                        if json_str == '[DONE]':
                            break
                        try:
                            data = json.loads(json_str)
                            if 'choices' in data:
                                content = data['choices'][0]['delta'].get('content', '')
                                if content:
                                    print(content, end='', flush=True)
                        except:
                            pass
            return ""
        else:
            result = response.json()
            return result['choices'][0]['message']['content']
    
    def _gemini_chat(self, prompt: str, stream: bool) -> str:
        """Gemini chat implementation"""
        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=stream
        )
        response.raise_for_status()
        
        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'candidates' in data:
                            text = data['candidates'][0]['content']['parts'][0].get('text', '')
                            if text:
                                print(text, end='', flush=True)
                    except:
                        pass
            return ""
        else:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']

# Usage
# Using OpenAI
openai_client = UnifiedAIClient("openai", "YOUR_OPENAI_KEY")
response1 = openai_client.chat("Hello!")

# Using Gemini
gemini_client = UnifiedAIClient("gemini", "YOUR_GEMINI_KEY")
response2 = gemini_client.chat("Hello!")
```

---

## 💬 Part 4: Simple Chat Application

```python
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

# Interactive chat loop
def run_chatbot():
    """Run interactive chatbot"""
    print("🤖 AI Chatbot - Type 'quit' to exit\n")
    
    # Initialize (you can switch between "openai" or "gemini")
    bot = SimpleChatBot("openai", "YOUR_API_KEY")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Goodbye! 👋")
            break
        
        print("Bot: ", end='')
        response = bot.chat(user_input)
        print(response)
        print()

# Run chatbot
if __name__ == "__main__":
    run_chatbot()
```

---

## 🎯 Real-World Business Example

### Customer Support Bot

```python
class CustomerSupportBot:
    """Customer support chatbot"""
    
    def __init__(self, api_key: str):
        self.client = OpenAIClient(api_key)
        self.system_prompt = """You are a helpful customer support agent.
        Be polite, professional, and try to solve customer issues.
        If you cannot help, escalate to human support."""
    
    def handle_query(self, customer_query: str) -> str:
        """Handle customer query"""
        full_prompt = f"{self.system_prompt}\n\nCustomer: {customer_query}\n\nAgent:"
        response = self.client.chat(full_prompt)
        return response
    
    def categorize_query(self, query: str) -> str:
        """Categorize customer query"""
        categories = {
            "billing": ["payment", "invoice", "refund", "charge"],
            "technical": ["bug", "error", "not working", "broken"],
            "general": ["question", "help", "information"]
        }
        
        query_lower = query.lower()
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        return "general"

# Usage
support_bot = CustomerSupportBot("YOUR_API_KEY")

query = "I have a billing issue with my last payment"
category = support_bot.categorize_query(query)
print(f"Category: {category}")

response = support_bot.handle_query(query)
print(f"Response: {response}")
```

---

## 🎯 Key Takeaways

1. **Gemini API:** Google's AI, easy to use
2. **OpenAI API:** Most popular, powerful models
3. **Streaming:** Better user experience
4. **Error Handling:** Always handle API errors
5. **Unified Clients:** Support multiple providers

---

## 🚀 Next Steps

Ready to learn about security? Let's move to:
- **Section 6:** AI Basics & Security - Prompt Engineering

---

**Pro Tip:** Start with non-streaming, then add streaming for better UX! 🚀

![InavLabs Logo](../../public/images/inavlabs.png)

