from datetime import datetime
from typing import Any, Dict, Optional

from passlib.context import CryptContext
from sqlalchemy import func

from database.models.chat import Chat
from database.models.user import User
from database.session import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    def create_user(full_name: str, username: str, email: str, password: str, role: str = "user") -> User:
        with SessionLocal() as db:
            if UserService.get_user_by_username(username):
                raise ValueError("Username already registered")

            if UserService.get_user_by_email(email):
                raise ValueError("Email already registered")

            hashed_password = pwd_context.hash(password)
            new_user = User(
                full_name=full_name,
                username=username,
                email=email,
                password=hashed_password,
                role=role
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        with SessionLocal() as db:
            return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        with SessionLocal() as db:
            return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        with SessionLocal() as db:
            return db.query(User).filter(User.email == user_email).first()

    @staticmethod
    def update_user(
        user_id: int,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None
    ) -> bool:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False

            if full_name:
                user.full_name = full_name
            if email and email != user.email:
                if UserService.get_user_by_email(email):
                    raise ValueError("Email already in use")
                user.email = email
            if password:
                user.password = pwd_context.hash(password)
            if role:
                user.role = role

            user.updatedAt = datetime.utcnow()
            db.commit()
            db.refresh(user)
            return True

    @staticmethod
    def admin_update_user(
        user_id: int,
        full_name: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> bool:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False

            if full_name:
                user.full_name = full_name
            if username and username != user.username:
                if UserService.get_user_by_username(username):
                    raise ValueError("Username already in use")
                user.username = username
            if email and email != user.email:
                if UserService.get_user_by_email(email):
                    raise ValueError("Email already in use")
                user.email = email
            if password:
                user.password = pwd_context.hash(password)
            if role:
                user.role = role
            if is_active is not None:
                user.is_active = is_active

            user.updatedAt = datetime.utcnow()
            db.commit()
            db.refresh(user)
            return True

    @staticmethod
    def delete_user(user_id: int) -> bool:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False

            db.delete(user)
            db.commit()
            return True

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_username(username)
        if not user or not UserService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def get_users_info() -> Dict[str, Any]:
        with SessionLocal() as db:
            users_info = (
                db.query(
                    User.id,
                    User.full_name.label("name"),
                    User.email,
                    User.role,
                    func.count(Chat.id).label("questions_asked")
                )
                .outerjoin(Chat, User.id == Chat.user_id)
                .group_by(User.id)
                .all()
            )

            total_users = db.query(User).count()
            total_admins = db.query(User).filter(User.role == "admin").count()
            total_questions = db.query(func.count(Chat.id)).scalar() or 0

            return {
                "general_metrics": {
                    "total_users": total_users,
                    "total_admins": total_admins,
                    "total_questions_asked": total_questions
                },
                "users_info": [
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": user.role,
                        "questions_asked": user.questions_asked
                    }
                    for user in users_info
                ]
            }

    @staticmethod
    def promote_to_admin(user_id: int) -> bool:
        return UserService.admin_update_user(user_id, role="admin")
