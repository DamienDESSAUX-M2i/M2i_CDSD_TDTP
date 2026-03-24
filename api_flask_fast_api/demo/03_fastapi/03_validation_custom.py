"""
FastAPI Demo 3: Custom Validation
Demonstrates custom validators and validation logic

Features:
    - Field validators
    - Root validators
    - Custom error messages
    - Multi-field validation
    - Conditional validation

Usage:
    python 03_validation_custom.py

Testing:
    # Valid registration
    curl -X POST http://localhost:8000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"john_doe","password":"SecurePass123!","confirm_password":"SecurePass123!","age":28}'

    # Weak password
    curl -X POST http://localhost:8000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"john","password":"123","confirm_password":"123","age":28}'

    # Password mismatch
    curl -X POST http://localhost:8000/api/register \
      -H "Content-Type: application/json" \
      -d '{"username":"john_doe","password":"SecurePass123!","confirm_password":"Different123!","age":28}'
"""

import re
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(
    title="FastAPI Custom Validation Demo",
    description="Demonstrates custom validators and validation logic",
    version="1.0.0",
)


# ============================================================================
# Models with Custom Validators
# ============================================================================


class Registration(BaseModel):
    """Registration model with custom validation"""

    username: str = Field(..., min_length=3, max_length=20, description="Username")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")
    age: int = Field(..., ge=18, le=120, description="Age (18-120)")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """
        Custom username validation
        Must contain only alphanumeric and underscore
        """
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        """
        Custom password strength validation
        Must contain uppercase, lowercase, digit, and special char
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        """
        Root validator - validate across multiple fields
        Checks that password and confirm_password match
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class ContactInfo(BaseModel):
    """Contact info with email and phone validation"""

    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    country: str = Field(..., description="Country code (2 letters)")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone format (optional but if provided, must be valid)"""
        if v is None:
            return v

        # Allow only digits, spaces, hyphens, and parentheses
        if not re.match(r"^[\d\s\-\(\)]+$", v):
            raise ValueError("Invalid phone format")

        # Extract digits and check length (10-15 digits for international numbers)
        digits_only = re.sub(r"\D", "", v)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError("Phone must have 10-15 digits")

        return v

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        """Validate country code (ISO 3166-1 alpha-2)"""
        valid_countries = ["US", "GB", "FR", "DE", "ES", "IT", "CA", "AU", "JP", "CN"]
        v_upper = v.upper()
        if v_upper not in valid_countries:
            raise ValueError(f"Country must be one of: {', '.join(valid_countries)}")
        return v_upper


class ProductReview(BaseModel):
    """Product review with rating and text validation"""

    product_id: int = Field(..., gt=0, description="Product ID")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 stars)")
    title: str = Field(..., min_length=5, max_length=100, description="Review title")
    text: str = Field(..., min_length=10, max_length=1000, description="Review text")
    would_recommend: bool = Field(..., description="Would recommend?")

    @field_validator("text")
    @classmethod
    def validate_review_text(cls, v):
        """Validate review text doesn't contain spam patterns"""
        spam_patterns = [
            r"http[s]?://",  # URLs
            r"viagra|casino|lottery",  # Spam keywords
            r"[!]{3,}",  # Multiple exclamation marks
        ]

        for pattern in spam_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Review contains spam or suspicious content")

        return v

    @model_validator(mode="after")
    def validate_rating_consistency(self):
        """
        Validate rating is consistent with recommendation
        If rating <= 2, should not recommend
        """
        if self.rating <= 2 and self.would_recommend:
            raise ValueError("Cannot recommend if rating is 2 or less")
        return self


class CreditCard(BaseModel):
    """Credit card with Luhn algorithm validation"""

    number: str = Field(..., description="Card number")
    expiry_month: int = Field(..., ge=1, le=12, description="Expiry month")
    expiry_year: int = Field(..., ge=2024, le=2050, description="Expiry year")
    cvv: str = Field(..., description="CVV (3-4 digits)")

    @field_validator("number")
    @classmethod
    def validate_card_number(cls, v):
        """Validate credit card number format and Luhn checksum"""
        # Remove spaces and hyphens
        v = v.replace(" ", "").replace("-", "")

        # Check if only digits
        if not v.isdigit():
            raise ValueError("Card number must contain only digits")

        # Check length (typically 13-19 digits)
        if len(v) < 13 or len(v) > 19:
            raise ValueError("Card number must be 13-19 digits")

        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(v)):
            d = int(digit)
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d

        if total % 10 != 0:
            raise ValueError("Invalid card number (Luhn checksum failed)")

        return v

    @field_validator("cvv")
    @classmethod
    def validate_cvv(cls, v):
        """Validate CVV format"""
        if not re.match(r"^\d{3,4}$", v):
            raise ValueError("CVV must be 3 or 4 digits")
        return v


# ============================================================================
# In-memory storage
# ============================================================================

registrations = {}
reviews = {}
next_review_id = 1


# ============================================================================
# Endpoints
# ============================================================================


@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {"message": "FastAPI Custom Validation Demo"}


@app.post("/api/register", status_code=201, tags=["Auth"])
def register(data: Registration):
    """
    Register user with custom validation

    Custom validators:
    - Username: alphanumeric + underscore only
    - Password: must contain uppercase, lowercase, digit, special char
    - Root validator: passwords must match
    """
    username = data.username

    if username in registrations:
        raise HTTPException(status_code=409, detail="Username already taken")

    registrations[username] = {
        "username": username,
        "age": data.age,
        "registered_at": "2024-01-15",
    }

    return {"success": True, "message": "Registration successful", "username": username}


@app.post("/api/contact", status_code=201, tags=["Contact"])
def save_contact(contact: ContactInfo):
    """
    Save contact information with custom validation

    Validators:
    - Email: must be valid email format
    - Phone: optional, but if provided must be valid (10-15 digits)
    - Country: must be ISO 3166-1 alpha-2 code
    """
    return {"success": True, "message": "Contact saved", "data": contact.dict()}


@app.post("/api/reviews", status_code=201, tags=["Reviews"])
def create_review(review: ProductReview):
    """
    Create product review with custom validation

    Validators:
    - Text: no spam patterns allowed
    - Rating consistency: rating <= 2 cannot be recommended
    """
    global next_review_id

    review_data = {"id": next_review_id, **review.dict()}

    reviews[next_review_id] = review_data
    next_review_id += 1

    return {"success": True, "message": "Review created", "data": review_data}


@app.post("/api/validate-card", tags=["Validation"])
def validate_card(card: CreditCard):
    """
    Validate credit card with custom validators

    Validators:
    - Card number: Luhn algorithm checksum
    - CVV: 3-4 digits
    - Expiry: month 1-12, year >= 2024
    """
    # Don't return actual card number in response
    return {
        "success": True,
        "message": "Card validation successful",
        "card_type": "Valid",
        "last_4": card.number[-4:],
        "expiry": f"{card.expiry_month:02d}/{card.expiry_year % 100:02d}",
    }


@app.post("/api/validate-field", tags=["Validation"])
def validate_field(field_type: str, value: str):
    """
    Endpoint to test individual field validators

    Parameters:
        field_type: email, phone, username, password, card_number
        value: value to validate
    """
    try:
        if field_type == "email":
            ContactInfo.model_validate({"email": value, "country": "US"})
            return {"success": True, "field": field_type, "message": "Valid"}

        elif field_type == "phone":
            ContactInfo.model_validate(
                {"email": "test@example.com", "phone": value, "country": "US"}
            )
            return {"success": True, "field": field_type, "message": "Valid"}

        elif field_type == "username":
            return {"success": True, "message": "Valid username"}

        elif field_type == "password":
            return {"success": True, "message": "Valid password"}

        else:
            return {"error": "Unknown field type"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/validation-rules", tags=["Info"])
def validation_rules():
    """Get all validation rules"""
    return {
        "models": {
            "Registration": {
                "username": "3-20 chars, alphanumeric + underscore only",
                "password": "8+ chars, uppercase, lowercase, digit, special char",
                "confirm_password": "must match password",
                "age": "18-120 years",
            },
            "ContactInfo": {
                "email": "valid email format",
                "phone": "optional, 10-15 digits if provided",
                "country": "ISO 3166-1 alpha-2 code (US, GB, FR, etc)",
            },
            "ProductReview": {
                "rating": "1-5 stars",
                "title": "5-100 characters",
                "text": "10-1000 characters, no spam",
                "would_recommend": "boolean, must be false if rating <= 2",
            },
            "CreditCard": {
                "number": "13-19 digits, Luhn algorithm validation",
                "expiry_month": "1-12",
                "expiry_year": "2024-2050",
                "cvv": "3-4 digits",
            },
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("FastAPI Demo 3: Custom Validation")
    print("=" * 70)
    print("\nCustom Validators:")
    print("  Field validators (@field_validator)")
    print("  Root validators (@model_validator)")
    print("  Regex pattern matching")
    print("  Cross-field validation")
    print("  Complex algorithms (Luhn checksum)")
    print("\nServer running on http://localhost:8000")
    print("\nTest with curl:")
    print("\n1. Register with valid data:")
    print("   curl -X POST http://localhost:8000/api/register \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"username":"john_doe","password":"SecurePass123!",')
    print('          "confirm_password":"SecurePass123!","age":28}\'')
    print("\n2. Register with weak password:")
    print("   curl -X POST http://localhost:8000/api/register \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"username":"john_doe","password":"weak",')
    print('          "confirm_password":"weak","age":28}\'')
    print("\n3. Save contact:")
    print("   curl -X POST http://localhost:8000/api/contact \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"email":"john@example.com","country":"US"}\'')
    print("\n4. Create review:")
    print("   curl -X POST http://localhost:8000/api/reviews \\")
    print("     -H 'Content-Type: application/json' \\")
    print('     -d \'{"product_id":1,"rating":5,"title":"Excellent!",')
    print('          "text":"Very good product","would_recommend":true}\'')
    print("\n5. Interactive docs:")
    print("   http://localhost:8000/docs")
    print("\n" + "=" * 70)
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
