from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    Registration request payload.
    - Email validated as real email format
    - Password min 8 chars (basic policy)
    - full_name 2-120 chars
    - role: buyer ya seller (admin publicly nahi banta)
    """

    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=120)
    role: str = Field(pattern="^(buyer|seller)$")

    # Seller-only optional fields
    store_name: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginResponse(TokenResponse):
    """Login ke baad token + user dono."""
    user: "UserResponse"


# Circular import avoid karne ke liye import end me
from app.schemas.user import UserResponse  # noqa: E402
LoginResponse.model_rebuild()




