# 4. APIs, WebSockets & HTTP Streaming

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

## 🎯 Learning Objectives

By the end of this section, you'll:
- Understand REST APIs and how to use them
- Learn WebSocket protocol for real-time communication
- Master HTTP streaming for AI responses
- Build practical API integrations

---

## 🌐 Part 1: REST APIs - The Foundation

### What is an API?

**API = Application Programming Interface**

**Real-world analogy:** 
- **Restaurant Menu:** You (client) order food (request) → Kitchen (server) prepares → Waiter (API) brings food (response)
- **API:** Your code requests data → Server processes → API returns data

### How APIs Work

```
Your Code → HTTP Request → API Server → Process → HTTP Response → Your Code
```

### Making API Requests with Python

```python
import requests

# GET request (fetching data)
response = requests.get("https://api.example.com/users")
data = response.json()
print(data)

# POST request (sending data)
payload = {
    "name": "Rajesh",
    "email": "rajesh@example.com"
}
response = requests.post("https://api.example.com/users", json=payload)
result = response.json()
print(result)
```

**Business Application:** 
- **E-commerce:** Fetching product data from inventory API
- **Payment:** Processing payments via payment gateway API
- **AI Services:** Getting AI responses from OpenAI, Google APIs

---

### API Authentication

Most AI APIs require authentication:

```python
import requests

# Using API Key in headers
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.openai.com/v1/models",
    headers=headers
)

print(response.json())
```

---

## 🔌 Part 2: WebSockets - Real-Time Communication

### Why WebSockets?

**HTTP (REST):** 
- Request → Response → Connection closes
- Like sending letters: write, send, wait, receive

**WebSocket:**
- Persistent connection
- Both sides can send messages anytime
- Like a phone call: continuous conversation

**Real-world analogy:**
- **HTTP:** Asking "What's the weather?" → Getting answer → Done
- **WebSocket:** Opening weather app → Continuous updates every second

### WebSocket Use Cases

1. **Chat Applications:** Real-time messaging
2. **Live Updates:** Stock prices, notifications
3. **Gaming:** Real-time multiplayer
4. **AI Chatbots:** Streaming responses

### WebSocket in Python

```python
import asyncio
import websockets
import json

async def chat_client():
    """Connect to WebSocket server"""
    uri = "ws://localhost:8765"
    
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            "type": "message",
            "content": "Hello, AI!"
        }))
        
        # Receive response
        response = await websocket.recv()
        data = json.loads(response)
        print(f"Received: {data}")

# Run client
asyncio.run(chat_client())
```

**Business Application:**
- **Customer Support:** Real-time chat with support agents
- **Trading Platforms:** Live price updates
- **Collaboration Tools:** Real-time document editing

---

## 📡 Part 3: HTTP Streaming - AI Responses

### Why Streaming?

**Traditional HTTP:**
- Send request → Wait → Get complete response
- Problem: AI responses can take 10-30 seconds!

**HTTP Streaming:**
- Send request → Get response word-by-word as it's generated
- Like watching a video: starts playing immediately, not after download

### Streaming with Requests

```python
import requests

def stream_ai_response(prompt):
    """Stream AI response word by word"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # Enable streaming!
    }
    
    # Stream response
    response = requests.post(url, json=data, headers=headers, stream=True)
    
    for line in response.iter_lines():
        if line:
            # Parse streaming data
            decoded = line.decode('utf-8')
            if decoded.startswith('data: '):
                json_str = decoded[6:]  # Remove 'data: ' prefix
                if json_str != '[DONE]':
                    try:
                        import json
                        chunk = json.loads(json_str)
                        # Extract text from chunk
                        if 'choices' in chunk:
                            delta = chunk['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                print(content, end='', flush=True)
                    except:
                        pass

# Usage
stream_ai_response("Tell me a story about AI")
```

**Business Application:**
- **Chatbots:** Users see responses immediately
- **Code Generation:** See code being written in real-time
- **Content Creation:** Watch articles being generated

---

## 🔄 Protocols Explained Simply

### HTTP Protocol

**HTTP = HyperText Transfer Protocol**

```
Client Request:
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer token123

Server Response:
HTTP/1.1 200 OK
Content-Type: application/json
{"users": [...]}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Resource doesn't exist
- `401 Unauthorized` - Need authentication
- `500 Server Error` - Server problem

### WebSocket Protocol

**WebSocket = Persistent, bidirectional connection**

```
Client: "I want to upgrade to WebSocket"
Server: "OK, connection upgraded"
Client: "Hello!"
Server: "Hi there!"
Client: "How are you?"
Server: "Great!"
... (connection stays open)
```

**Key Difference:**
- HTTP: One request, one response, connection closes
- WebSocket: Connection stays open, both can send anytime

---

## 💻 Practical Example: API Client Class

```python
import requests
from typing import Optional, Dict, Any

class APIClient:
    """Generic API client for AI services"""
    
    def __init__(self, base_url: str, api_key: str):
        """Initialize API client"""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise error if bad status
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def stream_post(self, endpoint: str, data: Dict[str, Any]):
        """Stream POST request"""
        url = f"{self.base_url}/{endpoint}"
        data["stream"] = True
        response = requests.post(url, json=data, headers=self.headers, stream=True)
        response.raise_for_status()
        return response

# Usage
client = APIClient(
    base_url="https://api.openai.com/v1",
    api_key="YOUR_API_KEY"
)

# Get models
models = client.get("models")
print(models)

# Chat completion
chat_data = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}]
}
response = client.post("chat/completions", chat_data)
print(response)
```

---

## 🎯 Real-World Business Example

### E-commerce API Integration

```python
import requests

class EcommerceAPI:
    """E-commerce platform API client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.ecommerce.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_products(self, category: str = None):
        """Fetch products"""
        url = f"{self.base_url}/products"
        params = {}
        if category:
            params["category"] = category
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def create_order(self, product_id: int, quantity: int):
        """Create new order"""
        url = f"{self.base_url}/orders"
        data = {
            "product_id": product_id,
            "quantity": quantity
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# Usage
api = EcommerceAPI("your_api_key")
products = api.get_products(category="electronics")
order = api.create_order(product_id=123, quantity=2)
```

---

## 🔐 Error Handling for APIs

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url: str, headers: dict, data: dict = None):
    """Safely call API with error handling"""
    try:
        if data:
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        # Check status code
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP Error: {e}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except RequestException as e:
        return {"success": False, "error": f"Request failed: {e}"}

# Usage
result = safe_api_call(
    url="https://api.example.com/data",
    headers={"Authorization": "Bearer token"}
)
print(result)
```

---

## 🎯 Key Takeaways

1. **REST APIs:** Request-response pattern, most common
2. **WebSockets:** Persistent connections for real-time
3. **HTTP Streaming:** Get responses as they're generated
4. **Error Handling:** Always handle API errors gracefully
5. **Authentication:** Most APIs need API keys/tokens

---

## 🚀 Next Steps

Ready to use real AI APIs? Let's move to:
- **Section 5:** Practical - Gemini & OpenAI Integration

---

**Pro Tip:** Start with simple GET requests, then move to POST, then try streaming! 🚀

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

