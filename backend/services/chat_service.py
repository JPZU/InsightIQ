from database.models.chat import Chat
from database.models.question import Question
from database.models.response import Response
from database.session import SessionLocal


class ChatService:
    @staticmethod
    def get_chat_by_id(chat_id: int) -> Chat:
        with SessionLocal() as db:
            return db.query(Chat).filter(Chat.id == chat_id).first()

    @staticmethod
    def get_chats(user_id: int):
        with SessionLocal() as db:
            return db.query(Chat).filter(Chat.user_id == user_id).all()

    @staticmethod
    def create_chat(user_id: int, name: str) -> Chat:
        with SessionLocal() as db:
            new_chat = Chat(user_id=user_id, name=name)
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            print(new_chat.createdAt, new_chat.updatedAt)
            return new_chat

    @staticmethod
    def get_chat_messages(chat_id: int, limit: int = 10):
        with SessionLocal() as db:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                return []

            questions = db.query(Question).filter(Question.chat_id == chat_id).order_by(Question.createdAt.desc()).limit(limit).all()
            responses = db.query(Response).filter(Response.chat_id == chat_id).order_by(Response.createdAt.desc()).limit(limit).all()

            messages = [
                {"type": "question", "content": q.content, "created_at": q.createdAt} for q in questions
            ] + [
                {"type": "response", "content": r.content, "created_at": r.createdAt} for r in responses
            ]

            messages.sort(key=lambda x: x["created_at"])
            return messages

    @staticmethod
    def delete_chat(chat_id: int) -> bool:
        with SessionLocal() as db:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                return False
            db.delete(chat)
            db.commit()
            return True

    @staticmethod
    def update_chat_name(chat_id: int, new_name: str) -> bool:
        with SessionLocal() as db:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                return False
            chat.name = new_name
            db.commit()
            db.refresh(chat)
            return True

    @staticmethod
    def clear_chat_messages(chat_id: int) -> bool:
        with SessionLocal() as db:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                return False

            db.query(Question).filter(Question.chat_id == chat_id).delete()
            db.query(Response).filter(Response.chat_id == chat_id).delete()

            db.commit()
            return True
