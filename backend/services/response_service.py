from database.models.response import Response
from database.session import SessionLocal


class ResponseService: 

    @staticmethod
    def create_response(chat_id: int, question_id: int, content: str) -> Response:
        with SessionLocal() as db:
            response = Response(
                content=content,
                chat_id=chat_id,
                question_id=question_id,
            )
            db.add(response)
            db.commit()
            db.refresh(response)
            return response
