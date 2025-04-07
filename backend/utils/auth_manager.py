from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from utils.env_manager import EnvManager


class AuthManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
    secret_key = EnvManager.get_jwt_secret_key()
    algorithm = EnvManager.get_jwt_algorithm()
    token_expire_minutes = EnvManager.get_jwt_expiration_time()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthManager.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return AuthManager.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=AuthManager.token_expire_minutes)
        
        to_encode.update({"exp": int(expire.timestamp())})
        
        encoded_jwt = jwt.encode(to_encode, AuthManager.secret_key, algorithm=AuthManager.algorithm)
        
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            print(f"Token recibido: {token}")
            print(f"Secret key: {AuthManager.secret_key[:5]}...")
            print(f"Algoritmo: {AuthManager.algorithm}")
            
            payload = jwt.decode(
                token,
                AuthManager.secret_key,
                algorithms=[AuthManager.algorithm]
            )
            print(f"Payload decodificado: {payload}")
            
            user_id: str = payload.get("sub")
            if user_id is None:
                print("No se encontró 'sub' en el payload")
                raise credentials_exception
                
            return int(user_id)
        except JWTError as e:
            print(f"Error JWT: {str(e)}")
            raise credentials_exception
