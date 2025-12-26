"""
Pydantic & Type Hints Example
Reference: docs/session_1/3_advanced_python_oop.md
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal

class UserInput(BaseModel):
    """User input model with validation"""
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=18, le=100)  # ge = greater or equal
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[str] = "user"
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()  # Capitalize first letter


class AIConfig(BaseModel):
    """AI model configuration"""
    model_config = ConfigDict(frozen=True)  # Makes it immutable
    
    model_name: Literal["gpt-4", "gpt-3.5", "claude"] = "gpt-4"
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1, le=4000)
    system_prompt: str = "You are a helpful assistant."


# Example usage
if __name__ == "__main__":
    # Valid user input
    try:
        user1 = UserInput(
            name="rajesh kumar",
            age=25,
            email="rajesh@example.com"
        )
        print(f"Valid user: {user1.name}, {user1.email}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Invalid user input
    try:
        user2 = UserInput(
            name="",  # Too short
            age=15,   # Too young
            email="invalid-email"
        )
    except Exception as e:
        print(f"Validation error: {e}")
    
    # AI Config
    config = AIConfig(
        model_name="gpt-4",
        temperature=0.8,
        max_tokens=2000
    )
    print(f"Model: {config.model_name}, Temperature: {config.temperature}")

