import base64
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
import bcrypt
from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    Depends,
    HTTPException,
    Response,
    Header,
)
from fastapi.middleware.cors import CORSMiddleware
from inference import classify_image
import uuid
from sqlalchemy.orm import Session
from database import database, models, schemas, crud
from utils import jwtService
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "15"
)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO : Connect Backend to Front End
# TODO : Receive Image from From Front End and Save it in data Folder
# TODO : Analyze that image and send the result
# TODO : Modify UI and Backend Endpoints
# TODO : Modify Machine Learning Process

imgPath = "data/test"


@app.get("/")
async def root():
    classified = classify_image("data/test/test1.jpg")
    return f"{classified}"


@app.post("/classify")
async def classifyImage(file: UploadFile = File(...), gemType: str = Form(...)):
    print("Gem", gemType)
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    with open(f"{imgPath}/{file.filename}", "wb") as f:
        f.write(contents)

    #############################################
    # newImg = cv2.imread(f"{imgPath}/test1.jpg")
    # cv2.imwrite(f"{imgPath}/new.jpg",newImg)

    classified = classify_image(f"{imgPath}/{file.filename}")
    return {
        "result": classified["State"],
        "filename": file.filename,
        "gemType": gemType,
    }


@app.post("/save")
async def saveResult(
    response: Response,
    result: schemas.Result,
    authorization: Annotated[str, Header()],
    db: Session = Depends(get_db),
):
    requested_user = await jwtService.verify_token(authorization.split(" ")[1])
    print("Requested User", requested_user.id)
    # Send random gem type and satisfactory level for now
    print("Result", result)
    db_result = crud.save_result(db=db, result=result, user_id=requested_user.id)
    return {"data": db_result}


def encode_image(image_path):
    """Encodes image to Base64 if it exists."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return None


@app.get("/history")
async def getHistory(
    authorization: Annotated[str, Header()],
    db: Session = Depends(get_db),
):
    requested_user = await jwtService.verify_token(authorization.split(" ")[1])
    results = crud.get_results(db=db, user_id=requested_user.id)
    print("Result", results)
    # Attach image paths
    for gem in results:
        image_path = os.path.join(imgPath, gem.name)
        if os.path.exists(image_path):  # Ensure the file exists
            image_data = encode_image(image_path=image_path)
            gem.image = image_data
        else:
            gem.image = None  # Set None or a default image path if not found

    return {"data": results}


@app.post("/login")
async def login(
    response: Response,
    user: schemas.UserLogIn,
    db: Session = Depends(get_db),
):
    if not ACCESS_TOKEN_EXPIRE_MINUTES.isdigit():
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a valid number.")
    db_user = crud.get_user_by_email(db, email=user.email)
    if not bcrypt.checkpw(
        bytes(user.password, "utf-8"), bytes(db_user.password, "utf-8")
    ):
        print("Password is Incorrect")
        raise HTTPException(status_code=400, detail="Password is Incorrect")
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = jwtService.create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="accessToken",
        value=access_token,
        expires=datetime.now(timezone.utc) + access_token_expires,
        domain="localhost",
        samesite="lax",
        secure=False,
        max_age=9999,
    )
    return {"message": "Logged In Successfully", "data": db_user}


@app.post("/signup", response_model=schemas.User)
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("User Details", user)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    salt = bcrypt.gensalt(rounds=15)
    hashed_password = bcrypt.hashpw(bytes(user.password, "utf-8"), salt)
    user.password = hashed_password
    # Hash and salt the Password before sending it to create User
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}/", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
