from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from services.user_service import UserService
from utils.base_schema import BaseResponse
from utils.auth_manager import AuthManager

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthManager.create_access_token(
        data={"sub": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: int = Depends(AuthManager.get_current_user)):
    new_token = AuthManager.create_access_token(
        data={"sub": str(current_user)}
    )
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/logout", response_model=BaseResponse)
async def logout(current_user: int = Depends(AuthManager.get_current_user)):
    return BaseResponse(success=True, message="Successfully logged out")
