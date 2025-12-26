"""
Math Fundamentals: Softmax, Tokenization, Temperature
Reference: docs/session_1/8_math_fundamentals.md
"""

import math
import numpy as np
import random


def softmax(scores):
    """Calculate softmax probabilities"""
    # Step 1: Calculate exponentials
    exp_scores = [math.exp(score) for score in scores]
    
    # Step 2: Calculate sum
    sum_exp = sum(exp_scores)
    
    # Step 3: Calculate probabilities
    probabilities = [exp / sum_exp for exp in exp_scores]
    
    return probabilities


def softmax_numpy(scores):
    """Softmax using NumPy"""
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores)


def apply_temperature(logits, temperature=1.0):
    """Apply temperature to logits"""
    # Divide by temperature
    scaled_logits = logits / temperature
    
    # Apply softmax
    exp_scores = np.exp(scaled_logits)
    probabilities = exp_scores / np.sum(exp_scores)
    
    return probabilities


def word_tokenize(text):
    """Simple word tokenization"""
    return text.split()


def char_tokenize(text):
    """Character-level tokenization"""
    return list(text)


def analyze_tokens(text):
    """Analyze tokenization statistics"""
    words = text.split()
    
    stats = {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        "total_characters": len(text),
        "characters_per_word": len(text.replace(" ", "")) / len(words) if words else 0
    }
    
    return stats


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


# Example usage
if __name__ == "__main__":
    # Softmax example
    scores = [5, 3, 2]
    probabilities = softmax(scores)
    print("Softmax Example:")
    print(f"Scores: {scores}")
    print(f"Probabilities: {[f'{p:.3f}' for p in probabilities]}")
    print(f"Sum: {sum(probabilities):.3f}\n")
    
    # Temperature example
    word_logits = np.array([5.0, 3.0, 2.0, 1.0])
    words = ["hello", "hi", "hey", "greetings"]
    
    print("Temperature Effects:")
    for temp in [0.5, 1.0, 2.0]:
        probs = apply_temperature(word_logits, temperature=temp)
        print(f"\nTemperature {temp}:")
        for word, prob in zip(words, probs):
            print(f"  {word}: {prob:.2%}")
    
    # Tokenization example
    text = "Hello world! How are you? Hello again."
    stats = analyze_tokens(text)
    print(f"\nTokenization Stats: {stats}")
    
    # Text generation example
    print("\nText Generation:")
    generator_low = SimpleTextGenerator(temperature=0.3)
    generator_high = SimpleTextGenerator(temperature=1.5)
    
    print("Low Temperature (Focused):")
    print(generator_low.generate("Hello world", length=5))
    
    print("\nHigh Temperature (Creative):")
    print(generator_high.generate("Hello world", length=5))

