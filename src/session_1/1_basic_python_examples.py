"""
Basic Python Examples for AI
Reference: docs/session_1/2_python_for_ai.md
"""

# Variables & Data Types
age = 25
price = 99.99
is_active = True
name = "Rajesh"
message = f"Hello, {name}! You are {age} years old."

# Lists
fruits = ["apple", "banana", "orange"]
fruits.append("mango")

# Dictionaries
student = {
    "name": "Priya",
    "age": 22,
    "grades": [85, 90, 88]
}

# List comprehensions
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Functions
def greet(name):
    """Simple greeting function"""
    return f"Hello, {name}!"

def calculate_total(price, tax=0.18, discount=0):
    """Calculate total with tax and discount"""
    subtotal = price * (1 - discount)
    total = subtotal * (1 + tax)
    return total

# Error handling
def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Please provide numbers!")
        return None

# File operations
import json

def save_config(config, filename="config.json"):
    """Save configuration to JSON file"""
    with open(filename, "w") as file:
        json.dump(config, file, indent=2)

def load_config(filename="config.json"):
    """Load configuration from JSON file"""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Example usage
if __name__ == "__main__":
    print(greet("World"))
    print(calculate_total(1000))
    
    config = {
        "model": "gpt-4",
        "temperature": 0.7
    }
    save_config(config)
    loaded = load_config()
    print(loaded)

