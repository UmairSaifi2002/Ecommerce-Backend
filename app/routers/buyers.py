from typing import Annotated

from fastapi import APIRouter, Depends

from app.config.constants import UserRole
from app.schemas.user import UserResponse
from app.utils.security import require_role

router = APIRouter(prefix="/buyers", tags=["buyers"])


@router.get("/me", response_model=UserResponse)
async def buyer_me(
    user: Annotated[object, Depends(require_role(UserRole.BUYER))],
) -> UserResponse:
    """
    Buyer-only endpoint.
    Try with seller token → 403 Forbidden.
    """
    return UserResponse.model_validate(user)



