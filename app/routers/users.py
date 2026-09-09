from fastapi import APIRouter, Depends

from app.schemas.auth import UserResponse
from app.security.auth import get_current_user, require_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/admin-test")
def admin_test(
    current_user=Depends(require_admin)
):
    return {
        "message": "You are an admin",
        "user": current_user.name
    }