from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return {"message": "This is a users endpoint"}