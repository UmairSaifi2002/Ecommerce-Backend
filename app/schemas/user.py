from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class BuyerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    current_tier: str
    stripe_customer_id: str | None = None


class SellerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_name: str
    stripe_account_id: str | None = None
    kyc_status: str


class UserResponse(BaseModel):
    """
    Public user representation.
    hashed_password KABHI include nahi.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    # Optional profiles — role ke hisaab se populated
    buyer_profile: BuyerProfileResponse | None = None
    seller_profile: SellerProfileResponse | None = None




    