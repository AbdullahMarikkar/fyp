import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from src.database import database, models
from dotenv import load_dotenv
from src.controllers import user_controller, classify_controller
from src.middleware import authorize_middleware
from starlette.exceptions import HTTPException as StarletteHTTPException

# TODO : Add Remove Record From History method and make sure to add appropriate CRUD Operations
# TODO : Improve Error Handling and Polish as much as you can

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
    "ACCESS_TOKEN_EXPIRE_MINUTES", "15"
)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return {
        "status_code": exc.status_code,
        "content": {"error": "Client Error", "message": exc.detail},
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return {
        "status_code": 422,
        "content": {"error": "Validation Error", "message": exc.errors()},
    }


@app.exception_handler(Exception)
async def generic_exception_handler(response: Response, exc: Exception):
    return {
        "status_code": 500,
        "content": {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    }


app.add_middleware(authorize_middleware.AuthMiddleware)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
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


imgPath = "data/test"


app.include_router(user_controller.router, prefix="/users", tags=["Users"])
app.include_router(
    classify_controller.router, prefix="/classify", tags=["Classification"]
)


@app.get("/", tags=["Root"])
async def root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Gemstone Classification API!"}


# @app.post("/classify")
# async def classifyImage(file: UploadFile = File(...), gemType: str = Form(...)):
#     file.filename = f"{uuid.uuid4()}.jpg"
#     contents = await file.read()
#     with open(f"{imgPath}/{file.filename}", "wb") as f:
#         f.write(contents)

#     classified = classify_image(f"{imgPath}/{file.filename}")
#     return {
#         "result": classified["State"],
#         "filename": file.filename,
#         "gemType": gemType,
#     }


# @app.post("/save")
# async def saveResult(
#     response: Response,
#     result: schemas.Result,
#     authorization: Annotated[str, Header()],
#     db: Session = Depends(get_db),
# ):
#     requested_user = await jwtService.verify_token(authorization.split(" ")[1])
#     print("Requested User", requested_user.id)
#     # Send random gem type and satisfactory level for now
#     print("Result", result)
#     db_result = crud.save_result(db=db, result=result, user_id=requested_user.id)
#     return {"data": db_result}


# def encode_image(image_path):
#     """Encodes image to Base64 if it exists."""
#     if os.path.exists(image_path):
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode("utf-8")
#     return None


# @app.get("/history")
# async def getHistory(
#     authorization: Annotated[str, Header()],
#     db: Session = Depends(get_db),
# ):
#     requested_user = await jwtService.verify_token(authorization.split(" ")[1])
#     results = crud.get_results(db=db, user_id=requested_user.id)
#     print("Result", results)
#     # Attach image paths
#     for gem in results:
#         image_path = os.path.join(imgPath, gem.name)
#         if os.path.exists(image_path):  # Ensure the file exists
#             image_data = encode_image(image_path=image_path)
#             gem.image = image_data
#         else:
#             gem.image = None  # Set None or a default image path if not found

#     return {"data": results}


# @app.post("/login")
# async def login(
#     response: Response,
#     user: schemas.UserLogIn,
#     db: Session = Depends(get_db),
# ):
#     if not ACCESS_TOKEN_EXPIRE_MINUTES.isdigit():
#         raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a valid number.")
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if not db_user or not bcrypt.checkpw(
#         bytes(user.password, "utf-8"), bytes(db_user.password, "utf-8")
#     ):
#         print("Password is Incorrect")
#         raise HTTPException(status_code=400, detail="Password is Incorrect")
#     access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
#     access_token = jwtService.create_access_token(
#         data={"sub": db_user.email}, expires_delta=access_token_expires
#     )
#     response.set_cookie(
#         key="accessToken",
#         value=access_token,
#         expires=datetime.now(timezone.utc) + access_token_expires,
#         domain="localhost",
#         samesite="lax",
#         secure=False,
#         max_age=9999,
#     )
#     return {"message": "Logged In Successfully", "data": db_user}


# @app.post("/signup", response_model=schemas.User)
# def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     print("User Details", user)
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     salt = bcrypt.gensalt(rounds=15)
#     hashed_password = bcrypt.hashpw(bytes(user.password, "utf-8"), salt)
#     user.password = hashed_password
#     # Hash and salt the Password before sending it to create User
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}/", response_model=schemas.User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
