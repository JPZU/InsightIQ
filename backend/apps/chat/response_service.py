from fastapi import HTTPException
from database.session import SessionLocal
from database.models.response import Response


class ResponseService:

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
