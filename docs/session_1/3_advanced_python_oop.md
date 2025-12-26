# 3. Advanced Python for AI: OOP, Pydantic & Decorators

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

## 🎯 Learning Objectives

By the end of this section (30 minutes), you'll:
- Understand OOP as Agent Identities
- Master Pydantic for data validation
- Use Type Hints for better code
- Create and use Decorators for AI functions

---

## 🤖 Part 1: OOP as Agent Identities

### Why OOP for AI?

In AI, we often think of systems as **agents** - entities that can:
- Store information (attributes)
- Perform actions (methods)
- Make decisions (logic)

**Real-world analogy:** Think of a chatbot as a "Customer Service Agent"
- It has knowledge (training data)
- It can respond (methods)
- It makes decisions (which response to give)

### Basic Class Structure

```python
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

# Usage
agent = AIAgent("ChatBot", "gpt-4")
response = agent.respond("Hello!")
print(response)  # ChatBot says: I understand 'Hello!'
```

**Business Application:** Each customer service bot is an instance with its own memory!

---

### Inheritance: Specialized Agents

```python
class AIAgent:
    """Base AI agent"""
    
    def __init__(self, name):
        self.name = name
        self.knowledge_base = []
    
    def learn(self, information):
        """Agent learns new information"""
        self.knowledge_base.append(information)
    
    def respond(self, query):
        """Generic response"""
        return f"{self.name}: I'm processing your query..."

# Specialized agent
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

# Usage
legal_bot = LegalAgent("LegalAssistant")
response = legal_bot.respond("How to file taxes?")
print(response)
```

**Business Application:** Different agents for different departments (Sales, Support, Legal)

---

## 🛡️ Part 2: Pydantic & Type Hints

### Why Type Hints?

Type hints make code:
- **Clearer:** You know what data types to expect
- **Safer:** Catch errors before runtime
- **Better for AI:** APIs need strict data validation

### Basic Type Hints

```python
def process_text(text: str) -> str:
    """Process text and return processed version"""
    return text.upper()

def calculate_total(items: list[int]) -> float:
    """Calculate total from list of integers"""
    return sum(items) * 1.18  # Adding tax

# Usage
result1 = process_text("hello")  # "HELLO"
result2 = calculate_total([100, 200, 300])  # 708.0
```

---

### Pydantic: Data Validation

**Why Pydantic?** 
- Validates data automatically
- Prevents bugs
- Perfect for API requests/responses

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class UserInput(BaseModel):
    """User input model with validation"""
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=18, le=100)  # ge = greater or equal
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[str] = "user"
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()  # Capitalize first letter

# Usage - Valid data
user1 = UserInput(
    name="rajesh kumar",
    age=25,
    email="rajesh@example.com"
)
print(user1.name)  # "Rajesh Kumar" (auto-capitalized)

# Usage - Invalid data (will raise error)
try:
    user2 = UserInput(
        name="",  # Too short
        age=15,   # Too young
        email="invalid-email"
    )
except Exception as e:
    print(f"Error: {e}")
```

**Business Application:** Validating API inputs, ensuring data quality

---

### Pydantic for AI Configurations

```python
from pydantic import BaseModel
from typing import Literal

class AIConfig(BaseModel):
    """AI model configuration"""
    model_name: Literal["gpt-4", "gpt-3.5", "claude"] = "gpt-4"
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1, le=4000)
    system_prompt: str = "You are a helpful assistant."
    
    class Config:
        """Pydantic configuration"""
        frozen = True  # Makes it immutable

# Usage
config = AIConfig(
    model_name="gpt-4",
    temperature=0.8,
    max_tokens=2000
)

print(config.model_name)  # "gpt-4
# config.temperature = 1.5  # Error! (frozen)
```

---

## 🎨 Part 3: Decorators for AI Functions

### What are Decorators?

Decorators are like "wrappers" that add functionality to functions without changing the function itself.

**Real-world analogy:** Like adding a security guard to a building entrance - the building (function) stays the same, but now it's protected!

### Basic Decorator

```python
def log_calls(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_calls
def add_numbers(a, b):
    """Add two numbers"""
    return a + b

# Usage
result = add_numbers(5, 3)
# Output:
# Calling add_numbers with args: (5, 3)
# add_numbers returned: 8
```

---

### Decorator with Parameters

```python
def retry(max_attempts=3):
    """Decorator to retry failed operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed, retrying...")
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def call_api(url):
    """Call an API (might fail)"""
    # Simulating API call
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("API Error")
    return "Success!"

# Usage
result = call_api("https://api.example.com")
print(result)
```

---

### AI-Specific Decorators

#### 1. Rate Limiting Decorator

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """Limit API calls per minute"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def call_ai_api(prompt):
    """Call AI API with rate limiting"""
    print(f"Processing: {prompt}")
    return f"Response to: {prompt}"

# Usage
for i in range(5):
    call_ai_api(f"Query {i}")
```

#### 2. Input Validation Decorator

```python
from functools import wraps

def validate_input(*validators):
    """Validate function inputs"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate args
            for arg, validator in zip(args, validators):
                if not validator(arg):
                    raise ValueError(f"Invalid input: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_positive(x):
    """Check if number is positive"""
    return isinstance(x, (int, float)) and x > 0

def is_string(x):
    """Check if input is string"""
    return isinstance(x, str) and len(x) > 0

@validate_input(is_string, is_positive)
def process_order(customer_name, order_amount):
    """Process customer order"""
    return f"Order for {customer_name}: ₹{order_amount}"

# Usage
result = process_order("Rajesh", 1000)  # Valid
# result = process_order("", -100)  # Error!
```

#### 3. Caching Decorator (for AI responses)

```python
from functools import wraps

def cache_results(func):
    """Cache function results"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key
        key = str(args) + str(kwargs)
        
        # Check cache
        if key in cache:
            print(f"Cache hit for {func.__name__}!")
            return cache[key]
        
        # Call function and cache result
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"Cached result for {func.__name__}")
        return result
    
    return wrapper

@cache_results
def expensive_ai_call(prompt):
    """Simulate expensive AI API call"""
    print("Making expensive API call...")
    time.sleep(1)  # Simulating delay
    return f"AI Response to: {prompt}"

# Usage
result1 = expensive_ai_call("Hello")  # Makes API call
result2 = expensive_ai_call("Hello")  # Uses cache!
```

---

## 🎯 Complete Example: AI Agent with All Features

```python
from pydantic import BaseModel, Field
from typing import Optional
from functools import wraps
import time

# Pydantic Model
class AgentConfig(BaseModel):
    """Agent configuration"""
    name: str = Field(..., min_length=1)
    model: str = "gpt-4"
    temperature: float = Field(0.7, ge=0.0, le=2.0)

# Decorator
def log_interactions(func):
    """Log all agent interactions"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[{self.name}] Processing: {args[0] if args else 'No input'}")
        result = func(self, *args, **kwargs)
        print(f"[{self.name}] Response: {result}")
        return result
    return wrapper

# OOP Agent Class
class SmartAIAgent:
    """Advanced AI Agent with OOP, Pydantic, and Decorators"""
    
    def __init__(self, config: AgentConfig):
        """Initialize agent with validated config"""
        self.config = config
        self.name = config.name
        self.model = config.model
        self.memory = []
    
    @log_interactions
    def process(self, user_input: str) -> str:
        """Process user input"""
        response = f"{self.name} (using {self.model}): I understand '{user_input}'"
        self.memory.append({
            "input": user_input,
            "response": response,
            "timestamp": time.time()
        })
        return response
    
    def get_memory(self) -> list:
        """Get agent's memory"""
        return self.memory

# Usage
config = AgentConfig(name="LegalBot", model="gpt-4", temperature=0.5)
agent = SmartAIAgent(config)

response = agent.process("Can you help with legal advice?")
print(response)
```

---

## 💡 Real-World Business Example

### Customer Service Agent System

```python
from pydantic import BaseModel
from typing import Literal

class CustomerQuery(BaseModel):
    """Validated customer query"""
    customer_id: int
    query_type: Literal["support", "sales", "billing"]
    message: str = Field(..., min_length=5, max_length=500)

class CustomerServiceAgent:
    """Customer service agent"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.tickets_handled = 0
    
    def handle_query(self, query: CustomerQuery) -> str:
        """Handle customer query"""
        self.tickets_handled += 1
        
        if query.query_type == "support":
            return f"Support Agent {self.agent_id}: How can I help you?"
        elif query.query_type == "sales":
            return f"Sales Agent {self.agent_id}: Let me show you our products!"
        else:
            return f"Billing Agent {self.agent_id}: I'll check your account."

# Usage
query = CustomerQuery(
    customer_id=12345,
    query_type="support",
    message="My order is delayed"
)

agent = CustomerServiceAgent("CS-001")
response = agent.handle_query(query)
print(response)
```

---

## 🎯 Key Takeaways

1. **OOP = Agent Identities:** Classes represent agents with memory and behavior
2. **Pydantic = Data Safety:** Validates inputs automatically
3. **Type Hints = Clarity:** Makes code self-documenting
4. **Decorators = Power:** Add functionality without changing code

---

## 🚀 Next Steps

Ready to connect to real AI? Let's move to:
- **Section 4:** APIs, WebSockets, and HTTP Streaming

---

**Remember:** These concepts are the foundation of professional AI engineering! 💪

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

