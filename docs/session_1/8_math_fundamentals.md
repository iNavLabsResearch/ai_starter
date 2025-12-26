# 8. Math Fundamentals: Softmax, Tokenization & Temperature

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

## 🎯 Learning Objectives

By the end of this section, you'll:
- Understand the Softmax function
- Learn tokenization mathematics
- Master the temperature parameter
- See how these concepts apply to AI

---

## 📊 Part 1: Softmax Function

### What is Softmax?

**Softmax = Converts numbers into probabilities**

**Real-world analogy:**
- Like converting exam scores (0-100) into grades (A, B, C probabilities)
- Like a voting system where each option gets a probability

### Simple Explanation

Imagine you have 3 options and their "scores":
- Option A: 5 points
- Option B: 3 points  
- Option C: 2 points

Softmax converts these into probabilities:
- Option A: 70% chance
- Option B: 20% chance
- Option C: 10% chance

**Total = 100%** (all probabilities add up to 1)

### Mathematical Formula

```
Softmax(x_i) = e^(x_i) / Σ(e^(x_j)) for all j
```

**In simple terms:**
1. Take exponential (e^x) of each number
2. Sum all exponentials
3. Divide each exponential by the sum

### Python Implementation

```python
import math

def softmax(scores):
    """Calculate softmax probabilities"""
    # Step 1: Calculate exponentials
    exp_scores = [math.exp(score) for score in scores]
    
    # Step 2: Calculate sum
    sum_exp = sum(exp_scores)
    
    # Step 3: Calculate probabilities
    probabilities = [exp / sum_exp for exp in exp_scores]
    
    return probabilities

# Example
scores = [5, 3, 2]
probabilities = softmax(scores)

print("Scores:", scores)
print("Probabilities:", probabilities)
print("Sum:", sum(probabilities))  # Should be 1.0

# Output:
# Scores: [5, 3, 2]
# Probabilities: [0.84, 0.11, 0.05] (approximately)
# Sum: 1.0
```

### Using NumPy (Faster)

```python
import numpy as np

def softmax_numpy(scores):
    """Softmax using NumPy"""
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores)

# Example
scores = np.array([5, 3, 2])
probabilities = softmax_numpy(scores)
print(probabilities)
```

### Why Softmax in AI?

**AI Use Case:** When AI needs to choose between multiple options:

```python
# AI predicting next word
word_scores = {
    "hello": 8.5,
    "hi": 7.2,
    "hey": 6.1,
    "greetings": 2.3
}

# Convert to probabilities
scores_list = list(word_scores.values())
probabilities = softmax(scores_list)

# Create probability dictionary
word_probs = dict(zip(word_scores.keys(), probabilities))

print("Word Probabilities:")
for word, prob in word_probs.items():
    print(f"{word}: {prob:.2%}")
```

**Business Application:**
- **Recommendation Systems:** Probability of user liking each product
- **Classification:** Probability of email being spam
- **Language Models:** Probability of next word

---

## 🔤 Part 2: Tokenization Mathematics

### What is Tokenization?

**Tokenization = Breaking text into smaller pieces (tokens)**

**Real-world analogy:**
- Like cutting a pizza into slices
- Like breaking a sentence into words

### Types of Tokenization

#### 1. **Word-Level Tokenization**

```python
def word_tokenize(text):
    """Simple word tokenization"""
    return text.split()

# Example
text = "Hello world! How are you?"
tokens = word_tokenize(text)
print(tokens)
# ['Hello', 'world!', 'How', 'are', 'you?']

# Problem: Punctuation attached to words
```

#### 2. **Character-Level Tokenization**

```python
def char_tokenize(text):
    """Character-level tokenization"""
    return list(text)

# Example
text = "Hello"
tokens = char_tokenize(text)
print(tokens)
# ['H', 'e', 'l', 'l', 'o']
```

#### 3. **Subword Tokenization (BPE - Byte Pair Encoding)**

**Most common in modern AI!**

```python
# Simplified BPE example
def simple_bpe_tokenize(text, vocab_size=1000):
    """Simplified BPE tokenization"""
    # Start with character-level
    tokens = list(text)
    
    # Merge most frequent pairs
    # (This is simplified - real BPE is more complex)
    pairs = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i+1])
        pairs[pair] = pairs.get(pair, 0) + 1
    
    # Merge most common pair
    if pairs:
        most_common = max(pairs, key=pairs.get)
        # Merge logic here...
    
    return tokens

# Real-world: Use libraries like tiktoken (OpenAI) or sentencepiece
```

### Tokenization Math: Vocabulary Size

**Vocabulary = All possible tokens**

```python
# Example vocabulary
vocabulary = {
    "hello": 0,
    "world": 1,
    "how": 2,
    "are": 3,
    "you": 4,
    "<unk>": 5,  # Unknown token
    "<pad>": 6   # Padding token
}

def text_to_ids(text, vocab):
    """Convert text to token IDs"""
    words = text.lower().split()
    ids = []
    for word in words:
        ids.append(vocab.get(word, vocab["<unk>"]))
    return ids

# Example
text = "Hello world"
ids = text_to_ids(text, vocabulary)
print(ids)  # [0, 1]
```

### Tokenization Statistics

```python
def analyze_tokens(text):
    """Analyze tokenization statistics"""
    words = text.split()
    
    stats = {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "avg_word_length": sum(len(w) for w in words) / len(words),
        "total_characters": len(text),
        "characters_per_word": len(text.replace(" ", "")) / len(words)
    }
    
    return stats

# Example
text = "Hello world! How are you? Hello again."
stats = analyze_tokens(text)
print(stats)
```

**Business Application:**
- **Cost Calculation:** AI APIs charge per token
- **Model Size:** Larger vocabulary = larger model
- **Processing Speed:** More tokens = slower processing

---

## 🌡️ Part 3: Temperature Parameter

### What is Temperature?

**Temperature = Controls randomness in AI responses**

**Real-world analogy:**
- **Low Temperature (0.1-0.5):** Like a focused student - gives consistent, predictable answers
- **High Temperature (0.7-2.0):** Like a creative artist - gives varied, creative answers

### How Temperature Works

Temperature modifies probabilities before sampling:

```python
import numpy as np

def apply_temperature(logits, temperature=1.0):
    """Apply temperature to logits"""
    # Divide by temperature
    scaled_logits = logits / temperature
    
    # Apply softmax
    exp_scores = np.exp(scaled_logits)
    probabilities = exp_scores / np.sum(exp_scores)
    
    return probabilities

# Example: Word prediction
word_logits = np.array([5.0, 3.0, 2.0, 1.0])
words = ["hello", "hi", "hey", "greetings"]

# Low temperature (0.5) - More focused
probs_low = apply_temperature(word_logits, temperature=0.5)
print("Low Temperature (0.5):")
for word, prob in zip(words, probs_low):
    print(f"  {word}: {prob:.2%}")

# High temperature (2.0) - More random
probs_high = apply_temperature(word_logits, temperature=2.0)
print("\nHigh Temperature (2.0):")
for word, prob in zip(words, probs_high):
    print(f"  {word}: {prob:.2%}")
```

### Temperature Effects

```python
def demonstrate_temperature():
    """Demonstrate temperature effects"""
    scores = np.array([8.0, 5.0, 3.0, 1.0])
    
    temperatures = [0.1, 0.5, 1.0, 2.0]
    
    print("Temperature Effects:")
    print("-" * 50)
    
    for temp in temperatures:
        probs = apply_temperature(scores, temp)
        max_prob = max(probs)
        entropy = -np.sum(probs * np.log(probs + 1e-10))  # Measure of randomness
        
        print(f"\nTemperature: {temp}")
        print(f"  Max Probability: {max_prob:.2%}")
        print(f"  Entropy (randomness): {entropy:.3f}")
        print(f"  Probabilities: {[f'{p:.2%}' for p in probs]}")

demonstrate_temperature()
```

### Choosing Temperature

```python
# Temperature guidelines
TEMPERATURE_GUIDE = {
    "code_generation": 0.2,  # Very focused, deterministic
    "factual_qa": 0.3,        # Consistent answers
    "creative_writing": 0.8,   # Creative but coherent
    "brainstorming": 1.2,     # Very creative
    "random_exploration": 2.0  # Maximum creativity
}

def get_temperature_for_task(task_type: str) -> float:
    """Get recommended temperature for task"""
    return TEMPERATURE_GUIDE.get(task_type, 0.7)

# Usage
temp = get_temperature_for_task("code_generation")
print(f"Recommended temperature: {temp}")
```

---

## 🎯 Complete Example: AI Text Generation

```python
import numpy as np
import random

class SimpleTextGenerator:
    """Simple text generator demonstrating math concepts"""
    
    def __init__(self, temperature=0.7):
        self.temperature = temperature
        self.vocab = ["hello", "world", "ai", "is", "awesome", "cool"]
        self.vocab_size = len(self.vocab)
    
    def tokenize(self, text):
        """Simple tokenization"""
        return text.lower().split()
    
    def softmax(self, scores):
        """Calculate softmax"""
        exp_scores = np.exp(scores / self.temperature)
        return exp_scores / np.sum(exp_scores)
    
    def predict_next_word(self, context):
        """Predict next word using softmax and temperature"""
        # Simulate word scores (in real AI, these come from model)
        word_scores = np.random.randn(self.vocab_size) * 2
        
        # Apply softmax with temperature
        probabilities = self.softmax(word_scores)
        
        # Sample based on probabilities
        next_word_idx = np.random.choice(self.vocab_size, p=probabilities)
        next_word = self.vocab[next_word_idx]
        
        return next_word, probabilities
    
    def generate(self, prompt, length=5):
        """Generate text"""
        tokens = self.tokenize(prompt)
        generated = tokens.copy()
        
        for _ in range(length):
            context = " ".join(generated[-3:])  # Last 3 words
            next_word, probs = self.predict_next_word(context)
            generated.append(next_word)
        
        return " ".join(generated)

# Usage
generator_low = SimpleTextGenerator(temperature=0.3)
generator_high = SimpleTextGenerator(temperature=1.5)

print("Low Temperature (Focused):")
print(generator_low.generate("Hello world", length=5))

print("\nHigh Temperature (Creative):")
print(generator_high.generate("Hello world", length=5))
```

---

## 💡 Real-World Business Example

### E-commerce Product Description Generator

```python
class ProductDescriptionGenerator:
    """Generate product descriptions with controlled creativity"""
    
    def __init__(self, temperature=0.6):
        self.temperature = temperature
    
    def generate_description(self, product_name, features):
        """Generate product description"""
        # In real implementation, this would use an AI model
        # Here we demonstrate the concept
        
        # Lower temperature for factual products (electronics)
        if "electronic" in product_name.lower():
            temp = 0.3
        # Higher temperature for creative products (fashion)
        else:
            temp = 0.8
        
        # Generate with appropriate temperature
        # ... AI generation logic ...
        
        return f"Amazing {product_name} with {', '.join(features)}"

# Usage
generator = ProductDescriptionGenerator()
description = generator.generate_description(
    "Wireless Headphones",
    ["Noise Cancellation", "30hr Battery", "Premium Sound"]
)
print(description)
```

---

## 🎯 Key Takeaways

1. **Softmax:** Converts scores to probabilities (sum = 1)
2. **Tokenization:** Breaks text into processable units
3. **Temperature:** Controls randomness (low = focused, high = creative)
4. **Math Matters:** Understanding these helps optimize AI applications
5. **Business Impact:** Affects cost, quality, and user experience

---

## 🚀 Next Steps

Ready to build a complete product? Let's move to:
- **Section 9:** Product v1 - The Secure Intern Chatbot

---

**Remember:** Math is the language of AI! Understanding it makes you a better AI engineer! 📊

<img src="../../public/images/inavlabs.png" alt="InavLabs Logo" width="100" height="100">

