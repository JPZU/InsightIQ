from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.user_service import UserService
from utils.base_schema import BaseResponse
from utils.auth_manager import AuthManager

router = APIRouter()


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


@router.post("/", response_model=BaseResponse)
def register_user(user_data: UserCreate):
    try:
        user = UserService.create_user(
            full_name=user_data.full_name,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return BaseResponse(
            success=True,
            response={"id": user.id, "full_name": user.full_name, "username": user.username, "email": user.email}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=BaseResponse)
def get_my_profile(current_user: int = Depends(AuthManager.get_current_user)):
    user = UserService.get_user_by_id(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return BaseResponse(
        success=True,
        response={
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "created_at": user.createdAt
        }
    )


@router.put("/me", response_model=BaseResponse)
def update_my_profile(
    user_data: UserUpdate,
    current_user: int = Depends(AuthManager.get_current_user)
):
    try:
        success = UserService.update_user(
            user_id=current_user,
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password
        )
        if not success:
            raise HTTPException(status_code=404, detail="User not found")

        return BaseResponse(success=True, message="Profile updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/me", response_model=BaseResponse)
def delete_my_account(current_user: int = Depends(AuthManager.get_current_user)):
    success = UserService.delete_user(current_user)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return BaseResponse(success=True, message="Account deleted successfully")
