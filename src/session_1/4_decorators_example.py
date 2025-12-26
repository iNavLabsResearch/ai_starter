"""
Decorators for AI Functions
Reference: docs/session_1/3_advanced_python_oop.md
"""

import time
from functools import wraps

def log_calls(func):
    """Decorator to log function calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper


def retry(max_attempts=3):
    """Decorator to retry failed operations"""
    def decorator(func):
        @wraps(func)
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


# Example usage
@log_calls
def add_numbers(a, b):
    """Add two numbers"""
    return a + b


@retry(max_attempts=3)
def call_api(url):
    """Call an API (might fail)"""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("API Error")
    return "Success!"


@rate_limit(calls_per_minute=10)
def call_ai_api(prompt):
    """Call AI API with rate limiting"""
    print(f"Processing: {prompt}")
    return f"Response to: {prompt}"


@cache_results
def expensive_ai_call(prompt):
    """Simulate expensive AI API call"""
    print("Making expensive API call...")
    time.sleep(1)  # Simulating delay
    return f"AI Response to: {prompt}"


if __name__ == "__main__":
    # Test log_calls
    result = add_numbers(5, 3)
    
    # Test cache
    result1 = expensive_ai_call("Hello")
    result2 = expensive_ai_call("Hello")  # Should use cache

