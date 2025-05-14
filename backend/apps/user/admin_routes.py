from typing import Optional, Any
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.user_service import UserService
from utils.auth_manager import AuthManager
from utils.base_schema import BaseResponse

router = APIRouter()

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[RoleEnum] = None

def verify_admin(current_user_id: int):
    current_user = UserService.get_user_by_id(current_user_id)
    print(f"Current user: {current_user.role.value}")
    print(RoleEnum.ADMIN.value)
    if not current_user or current_user.role.value != RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

@router.get("")
def list_all_users(current_user: int = Depends(AuthManager.get_current_user)):
    verify_admin(current_user)
    users = UserService.get_users_info()
    return {"response": users}

@router.get("/{user_id}")
def get_user_details(
    user_id: int,
    current_user: int = Depends(AuthManager.get_current_user)
):
    verify_admin(current_user)
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.createdAt.isoformat(),
        "updated_at": user.updatedAt.isoformat()
    }

@router.put("/{user_id}")
def admin_update_user(
    user_id: int,
    user_data: AdminUserUpdate,
    current_user: int = Depends(AuthManager.get_current_user)
):
    verify_admin(current_user)
    try:
        success = UserService.admin_update_user(
            user_id=user_id,
            full_name=user_data.full_name,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role.value if user_data.role else None
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {"message": "User updated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{user_id}")
def admin_delete_user(
    user_id: int,
    current_user: int = Depends(AuthManager.get_current_user)
):
    verify_admin(current_user)
    if user_id == current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete your own account"
        )

    success = UserService.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"message": "User deleted successfully"}
