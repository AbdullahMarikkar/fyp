from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import schemas, database
from src.services import user_service

router = APIRouter()


# Dependency to get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=schemas.User)
async def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Handles user registration by calling the user service."""
    db_user = await user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(db=db, user=user)


@router.post("/login")
async def login_user(
    response: Response, user: schemas.UserLogIn, db: Session = Depends(get_db)
):
    """Handles user login and sets the access token cookie."""
    print("User Data", user)
    result = await user_service.login_for_access_token(db, user.email, user.password)
    print("Result", result)
    response.set_cookie(
        key="accessToken",
        value=result[0],
        httponly=False,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )
    return {"message": "Logged In Successfully", "data": result[1]}


@router.get("/history")
async def get_user_history(
    request: Request,
    db: Session = Depends(get_db),
):
    """Fetches classification history for the authenticated user."""
    user_payload = request.state.user
    results = await user_service.get_user_history_with_images(
        db=db, user_id=user_payload.id
    )
    return {"data": results}


@router.post("/history/save")
async def save_user_result(
    result: schemas.Result,
    request: Request,
    db: Session = Depends(get_db),
):
    """Saves a classification result to the user's history."""
    user_payload = request.state.user
    return await user_service.save_classification_result(
        db=db, result=result, user_id=user_payload.id
    )


@router.delete("/history/{id}")
async def delete_history_record(id: int, db: Session = Depends(get_db)):
    print("History ID", id)
    return await user_service.delete_history_record(db, id)
