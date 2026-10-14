from typing import Annotated

from fastapi import APIRouter, Depends

from app.config.constants import UserRole
from app.schemas.user import UserResponse
from app.utils.security import require_role

router = APIRouter(prefix="/sellers", tags=["sellers"])


@router.get("/me", response_model=UserResponse)
async def seller_me(
    user: Annotated[object, Depends(require_role(UserRole.SELLER))],
) -> UserResponse:
    """Seller-only endpoint."""
    return UserResponse.model_validate(user)


