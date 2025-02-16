from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth_example():
    return {"message": "This is an auth endpoint"}