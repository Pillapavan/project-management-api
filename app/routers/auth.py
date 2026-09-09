from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
import logging

from app.schemas.auth import UserResponse, RegisterRequest, LoginRequest
from app.database.connection import get_db
from app.services.auth_service import register_user,login_user

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        return register_user(
            db=db,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

    except ValueError as exc:
        logger.info("Database operation failed")
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    token = login_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if token is None:
        logging.error("Invalid email or password")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }