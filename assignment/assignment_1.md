# Assignment 1: Library Management System API

## 📚 The Story

You're building a REST API for a local library that wants to digitize their book lending system. The library needs to:
- Register books with details
- Register members
- Track book borrowing and returns
- Calculate late fees
- Get statistics about popular books

Your task is to build a FastAPI application that handles all these operations using **Pydantic models**, **decorators**, **functions**, and **REST endpoints**.

---

## 🎯 Learning Objectives

By completing this assignment, you will:
1. Create Pydantic models with validation
2. Write custom decorators for logging and validation
3. Implement business logic functions
4. Build FastAPI endpoints (GET, POST, PUT, DELETE)
5. Test APIs using curl commands

---

## 📋 Requirements

### 1. Pydantic Models

Create three Pydantic models:

**Book Model:**
- `id`: int (auto-generated)
- `title`: str (min 3, max 200 chars)
- `author`: str (min 2, max 100 chars)
- `isbn`: str (must match ISBN format: 10 or 13 digits with optional dashes)
- `published_year`: int (between 1000 and current year)
- `copies_available`: int (minimum 0)
- `total_copies`: int (minimum 1)

**Member Model:**
- `id`: int (auto-generated)
- `name`: str (min 2, max 100 chars)
- `email`: str (valid email format)
- `phone`: str (10 digits, optional dashes/spaces)
- `membership_date`: str (YYYY-MM-DD format)

**BorrowRecord Model:**
- `id`: int (auto-generated)
- `book_id`: int
- `member_id`: int
- `borrow_date`: str (YYYY-MM-DD)
- `due_date`: str (YYYY-MM-DD)
- `return_date`: Optional[str] (YYYY-MM-DD, None if not returned)
- `late_fee`: float (default 0.0, minimum 0)

### 2. Decorators

Create two decorators:

**`log_operation` decorator:**
- Logs function name, arguments, and return value
- Format: `[LOG] Function: {function_name} | Args: {args} | Result: {result}`

**`validate_availability` decorator:**
- Checks if a book has available copies before borrowing
- Raises `ValueError` with message "Book not available" if copies_available == 0
- Only applies to functions that borrow books

### 3. Business Logic Functions

**`calculate_late_fee(borrow_date: str, due_date: str, return_date: str) -> float`:**
- Calculate late fee: ₹5 per day after due date
- If return_date is None or before due_date, return 0.0
- Return calculated fee

**`is_book_available(book_id: int, books: dict) -> bool`:**
- Check if book exists and has available copies
- Return True if copies_available > 0, else False

**`get_popular_books(borrow_records: list, books: dict, limit: int = 5) -> list`:**
- Count borrows per book
- Return top N most borrowed books with their details

### 4. FastAPI Endpoints

**Books:**
- `POST /books` - Add a new book
- `GET /books` - Get all books
- `GET /books/{book_id}` - Get book by ID
- `PUT /books/{book_id}` - Update book details
- `DELETE /books/{book_id}` - Delete a book

**Members:**
- `POST /members` - Register a new member
- `GET /members` - Get all members
- `GET /members/{member_id}` - Get member by ID

**Borrowing:**
- `POST /borrow` - Borrow a book (requires book_id, member_id)
- `POST /return` - Return a book (requires borrow_record_id, return_date)
- `GET /borrow/active` - Get all active borrows (not returned)
- `GET /borrow/stats` - Get borrowing statistics

---

## 💡 Hints

1. **Pydantic Validation:**
   - Use `Field()` for constraints (min_length, max_length, ge, le)
   - Use `@field_validator` for custom validation (ISBN format, email)
   - Use `Optional` from typing for nullable fields

2. **Decorators:**
   - Use `@wraps(func)` from `functools` to preserve function metadata
   - Access function arguments using `*args` and `**kwargs`
   - Store decorator state in closure variables

3. **FastAPI:**
   - Use Pydantic models as request/response models
   - Use `status_code` parameter in route decorators
   - Return dictionaries or Pydantic models from endpoints
   - Use `HTTPException` for error handling

4. **Data Storage:**
   - Use in-memory dictionaries (books, members, borrow_records)
   - Auto-increment IDs starting from 1

---

## 📝 Template Code

Create a file `assignment_1.py` and fill in the code between the markers:

```python
"""
Library Management System API
Assignment 1: FastAPI with Pydantic, Decorators, and Functions
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Dict
from functools import wraps
from datetime import datetime
import re

app = FastAPI(title="Library Management API", version="1.0.0")

# ========== DATA STORAGE (In-memory) ==========
books_db: Dict[int, dict] = {}
members_db: Dict[int, dict] = {}
borrow_records_db: Dict[int, dict] = {}
book_id_counter = 1
member_id_counter = 1
borrow_id_counter = 1

# ========== YOUR CODE STARTS HERE ==========

# TODO 1: Create Pydantic Models
# - Book model with all required fields and validators
# - Member model with email and phone validation
# - BorrowRecord model with optional return_date

class Book(BaseModel):
    # YOUR CODE HERE
    pass

class Member(BaseModel):
    # YOUR CODE HERE
    pass

class BorrowRecord(BaseModel):
    # YOUR CODE HERE
    pass

# TODO 2: Create Decorators
# - log_operation: Logs function calls
# - validate_availability: Checks book availability

def log_operation(func):
    # YOUR CODE HERE
    pass

def validate_availability(func):
    # YOUR CODE HERE
    pass

# TODO 3: Create Business Logic Functions
# - calculate_late_fee
# - is_book_available
# - get_popular_books

def calculate_late_fee(borrow_date: str, due_date: str, return_date: Optional[str]) -> float:
    # YOUR CODE HERE
    pass

def is_book_available(book_id: int, books: Dict[int, dict]) -> bool:
    # YOUR CODE HERE
    pass

def get_popular_books(borrow_records: List[dict], books: Dict[int, dict], limit: int = 5) -> List[dict]:
    # YOUR CODE HERE
    pass

# ========== YOUR CODE ENDS HERE ==========

# ========== FASTAPI ENDPOINTS ==========

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    """Add a new book to the library"""
    global book_id_counter, books_db
    
    # YOUR CODE HERE
    # - Assign auto-increment ID
    # - Convert Pydantic model to dict
    # - Store in books_db
    # - Return created book with ID
    
    pass

@app.get("/books")
def get_all_books():
    """Get all books"""
    # YOUR CODE HERE
    # - Return list of all books from books_db
    pass

@app.get("/books/{book_id}")
def get_book(book_id: int):
    """Get book by ID"""
    # YOUR CODE HERE
    # - Check if book exists
    # - Return book or raise HTTPException 404
    pass

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    """Update book details"""
    # YOUR CODE HERE
    # - Check if book exists
    # - Update book in books_db
    # - Return updated book
    pass

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    """Delete a book"""
    # YOUR CODE HERE
    # - Check if book exists
    # - Delete from books_db
    # - Return 204 No Content
    pass

@app.post("/members", status_code=status.HTTP_201_CREATED)
def create_member(member: Member):
    """Register a new member"""
    global member_id_counter, members_db
    
    # YOUR CODE HERE
    # - Assign auto-increment ID
    # - Store in members_db
    # - Return created member with ID
    pass

@app.get("/members")
def get_all_members():
    """Get all members"""
    # YOUR CODE HERE
    pass

@app.get("/members/{member_id}")
def get_member(member_id: int):
    """Get member by ID"""
    # YOUR CODE HERE
    pass

@app.post("/borrow")
@validate_availability
@log_operation
def borrow_book(book_id: int, member_id: int):
    """Borrow a book"""
    global borrow_id_counter, borrow_records_db, books_db
    
    # YOUR CODE HERE
    # - Validate book and member exist
    # - Check book availability
    # - Create borrow record (borrow_date = today, due_date = 14 days later)
    # - Decrease copies_available
    # - Return borrow record
    pass

@app.post("/return")
@log_operation
def return_book(borrow_record_id: int, return_date: str):
    """Return a borrowed book"""
    global borrow_records_db, books_db
    
    # YOUR CODE HERE
    # - Find borrow record
    # - Calculate late fee using calculate_late_fee()
    # - Update return_date and late_fee
    # - Increase copies_available
    # - Return updated record
    pass

@app.get("/borrow/active")
def get_active_borrows():
    """Get all active (not returned) borrows"""
    # YOUR CODE HERE
    # - Filter borrow_records_db where return_date is None
    # - Return list of active borrows
    pass

@app.get("/borrow/stats")
def get_borrow_stats():
    """Get borrowing statistics"""
    # YOUR CODE HERE
    # - Use get_popular_books() to get top 5 books
    # - Count total borrows, active borrows
    # - Return statistics dictionary
    pass

# ========== ROOT ENDPOINT ==========
@app.get("/")
def root():
    return {
        "message": "Library Management API",
        "version": "1.0.0",
        "endpoints": {
            "books": "/books",
            "members": "/members",
            "borrow": "/borrow",
            "stats": "/borrow/stats"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📦 Requirements File

Create `requirements.txt`:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pydantic[email]>=2.0.0
```

---

## 🧪 Testing Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the FastAPI Server

```bash
# Option 1: Using uvicorn directly
uvicorn assignment_1:app --reload --port 8000

# Option 2: Run the Python file
python assignment_1.py
```

The server will start at `http://localhost:8000`

### Step 3: Test with curl Commands

Open a new terminal and run these commands:

**1. Check API is running:**
```bash
curl http://localhost:8000/
```

**2. Add a book:**
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Programming",
    "author": "John Doe",
    "isbn": "978-0134685991",
    "published_year": 2020,
    "copies_available": 5,
    "total_copies": 5
  }'
```

**3. Get all books:**
```bash
curl http://localhost:8000/books
```

**4. Get book by ID:**
```bash
curl http://localhost:8000/books/1
```

**5. Register a member:**
```bash
curl -X POST "http://localhost:8000/members" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "9876543210",
    "membership_date": "2024-01-15"
  }'
```

**6. Borrow a book:**
```bash
curl -X POST "http://localhost:8000/borrow?book_id=1&member_id=1" \
  -H "Content-Type: application/json"
```

**7. Get active borrows:**
```bash
curl http://localhost:8000/borrow/active
```

**8. Return a book:**
```bash
curl -X POST "http://localhost:8000/return?borrow_record_id=1&return_date=2024-02-01" \
  -H "Content-Type: application/json"
```

**9. Get borrowing statistics:**
```bash
curl http://localhost:8000/borrow/stats
```

**10. Update a book:**
```bash
curl -X PUT "http://localhost:8000/books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python Programming",
    "author": "John Doe",
    "isbn": "978-0134685991",
    "published_year": 2021,
    "copies_available": 3,
    "total_copies": 5
  }'
```

**11. Delete a book:**
```bash
curl -X DELETE "http://localhost:8000/books/1"
```

---

## ✅ Expected Output Examples

**Successful book creation:**
```json
{
  "id": 1,
  "title": "Python Programming",
  "author": "John Doe",
  "isbn": "978-0134685991",
  "published_year": 2020,
  "copies_available": 5,
  "total_copies": 5
}
```

**Borrowing statistics:**
```json
{
  "total_borrows": 10,
  "active_borrows": 3,
  "popular_books": [
    {
      "book_id": 1,
      "title": "Python Programming",
      "borrow_count": 5
    }
  ]
}
```

---

## 🎓 Evaluation Criteria

- ✅ All Pydantic models created with proper validation
- ✅ Decorators implemented and working
- ✅ Business logic functions correct
- ✅ All endpoints functional
- ✅ Proper error handling (404, 400, etc.)
- ✅ Code follows Python best practices
- ✅ All curl tests pass

---

## 📚 Additional Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Pydantic Docs: https://docs.pydantic.dev/
- Python Decorators: https://realpython.com/primer-on-python-decorators/

---

**Good luck! 🚀**

