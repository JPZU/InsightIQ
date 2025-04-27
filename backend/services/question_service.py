
from database.models.question import Question
from database.session import SessionLocal


class QuestionService:
    @staticmethod
    def create_question(chat_id: int, content: str) -> Question:
        with SessionLocal() as db:
            question = Question(
                content=content,
                chat_id=chat_id,
            )
            db.add(question)
            db.commit()
            db.refresh(question)
            return question
