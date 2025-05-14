from database.models.response import Response
from database.session import SessionLocal
from typing import Optional
from fastapi import HTTPException


class ResponseService:

    @staticmethod
    def create_response(
        chat_id: int,
        question_id: int,
        content: str,
        query_result: dict = None,
        rating: Optional[int] = None
    ) -> Response:
        with SessionLocal() as db:
            response = Response(
                content=content,
                query_result=query_result,
                chat_id=chat_id,
                question_id=question_id,
                rating=rating
            )
            db.add(response)
            db.commit()
            db.refresh(response)
            return response

    @staticmethod
    def update_response_with_result(
        response_id: int,
        query_result: dict
    ) -> Response:
        with SessionLocal() as db:
            response = db.query(Response).filter(Response.id == response_id).first()
            if response:
                response.query_result = query_result
                db.commit()
                db.refresh(response)
            return response

    @staticmethod
    def rate_response(response_id: int, rating: int) -> None:
        """
        Califica una respuesta ya existente. Solo permite calificar una vez.
        rating: 0 (negativo) o 1 (positivo)
        """
        with SessionLocal() as db:
            response = db.query(Response).filter(Response.id == response_id).first()

            if not response:
                raise HTTPException(status_code=404, detail="Response not found")

            if response.rating is not None:
                raise HTTPException(status_code=400, detail="You already rated this response")

            if rating not in [0, 1]:
                raise HTTPException(status_code=400, detail="Rating must be 0 or 1")

            response.rating = rating
            db.commit()
