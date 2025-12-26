"""
Math Fundamentals: Softmax, Tokenization, Temperature
Reference: docs/session_1/8_math_fundamentals.md
"""

import math
import numpy as np
import tiktoken


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
    """Apply temperature to logits
    
    Logits are raw scores from the AI model before applying softmax.
    They represent the model's confidence scores for each possible token.
    """
    # Divide by temperature
    scaled_logits = logits / temperature
    
    # Apply softmax
    exp_scores = np.exp(scaled_logits)
    probabilities = exp_scores / np.sum(exp_scores)
    
    return probabilities


def tokenize_with_bpe(text, model="gpt-3.5-turbo"):
    """Tokenize text using BPE (Byte Pair Encoding) with tiktoken
    
    BPE is the tokenization method used by OpenAI models.
    It breaks text into subword units that are efficient for AI processing.
    """
    # Initialize tiktoken encoder
    encoding = tiktoken.encoding_for_model(model)
    
    # Tokenize text
    tokens = encoding.encode(text)
    
    # Decode tokens back to see what they represent
    token_strings = [encoding.decode([token]) for token in tokens]
    
    return {
        "tokens": tokens,
        "token_strings": token_strings,
        "token_count": len(tokens),
        "text": text
    }


def analyze_bpe_tokenization(text, model="gpt-3.5-turbo"):
    """Analyze BPE tokenization statistics"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    token_strings = [encoding.decode([token]) for token in tokens]
    
    stats = {
        "original_text": text,
        "original_length": len(text),
        "token_count": len(tokens),
        "tokens": tokens[:10],  # First 10 tokens
        "token_strings": token_strings[:10],  # First 10 token strings
        "tokens_per_character": len(tokens) / len(text) if text else 0,
        "vocabulary_size": encoding.n_vocab
    }
    
    return stats


class SimpleTextGenerator:
    """Simple text generator demonstrating math concepts"""
    
    def __init__(self, temperature=0.7):
        self.temperature = temperature
        self.vocab = ["hello", "world", "ai", "is", "awesome", "cool"]
        self.vocab_size = len(self.vocab)
    
    def softmax(self, logits):
        """Calculate softmax with temperature
        
        Logits are raw model scores before probability conversion.
        """
        exp_scores = np.exp(logits / self.temperature)
        return exp_scores / np.sum(exp_scores)
    
    def predict_next_word(self, context):
        """Predict next word using softmax and temperature"""
        # Simulate logits (raw scores from model)
        logits = np.random.randn(self.vocab_size) * 2
        
        # Apply softmax with temperature
        probabilities = self.softmax(logits)
        
        # Sample based on probabilities
        next_word_idx = np.random.choice(self.vocab_size, p=probabilities)
        next_word = self.vocab[next_word_idx]
        
        return next_word, probabilities, logits


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("SOFTMAX EXAMPLE")
    print("=" * 60)
    scores = [5, 3, 2]
    probabilities = softmax(scores)
    print(f"Scores: {scores}")
    print(f"Probabilities: {[f'{p:.3f}' for p in probabilities]}")
    print(f"Sum: {sum(probabilities):.3f}\n")
    
    print("=" * 60)
    print("TEMPERATURE EFFECTS (with Logits)")
    print("=" * 60)
    # Logits are raw scores from the model
    word_logits = np.array([5.0, 3.0, 2.0, 1.0])
    words = ["hello", "hi", "hey", "greetings"]
    
    print(f"Logits (raw model scores): {word_logits}")
    print()
    
    for temp in [0.5, 1.0, 2.0]:
        probs = apply_temperature(word_logits, temperature=temp)
        print(f"Temperature {temp}:")
        for word, prob in zip(words, probs):
            print(f"  {word}: {prob:.2%}")
        print()
    
    print("=" * 60)
    print("BPE TOKENIZATION WITH TIKTOKEN")
    print("=" * 60)
    
    # Example texts
    texts = [
        "Hello world!",
        "How are you doing today?",
        "Artificial Intelligence is amazing!",
        "The quick brown fox jumps over the lazy dog."
    ]
    
    for text in texts:
        result = tokenize_with_bpe(text)
        print(f"\nText: '{text}'")
        print(f"Token count: {result['token_count']}")
        print(f"Tokens: {result['tokens'][:10]}...")  # First 10 tokens
        print(f"Token strings: {result['token_strings'][:10]}...")  # First 10 token strings
    
    print("\n" + "=" * 60)
    print("BPE TOKENIZATION ANALYSIS")
    print("=" * 60)
    
    sample_text = "Hello! How are you? I'm learning about AI tokenization."
    stats = analyze_bpe_tokenization(sample_text)
    print(f"Original text: '{stats['original_text']}'")
    print(f"Original length: {stats['original_length']} characters")
    print(f"Token count: {stats['token_count']} tokens")
    print(f"Tokens per character: {stats['tokens_per_character']:.2f}")
    print(f"Vocabulary size: {stats['vocabulary_size']:,}")
    print(f"First 10 tokens: {stats['tokens']}")
    print(f"First 10 token strings: {stats['token_strings']}")
    
    print("\n" + "=" * 60)
    print("TEXT GENERATION WITH LOGITS")
    print("=" * 60)
    
    generator_low = SimpleTextGenerator(temperature=0.3)
    generator_high = SimpleTextGenerator(temperature=1.5)
    
    print("Low Temperature (Focused) - Logits converted to probabilities:")
    next_word, probs, logits = generator_low.predict_next_word("context")
    print(f"Logits: {logits}")
    print(f"Probabilities: {probs}")
    print(f"Selected word: {next_word}\n")
    
    print("High Temperature (Creative) - Logits converted to probabilities:")
    next_word, probs, logits = generator_high.predict_next_word("context")
    print(f"Logits: {logits}")
    print(f"Probabilities: {probs}")
    print(f"Selected word: {next_word}")
    
    print("\n✅ All examples completed successfully!")
