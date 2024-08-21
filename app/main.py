from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import schemas
import crud
import models
from database import get_db, engine

""" ------------------------------------------------------------------------------------------------- """
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Setup for tempaltes
templates = Jinja2Templates(directory="templates")

""" ------------------------------------------------------------------------------------------------- """
# Allowing all origins, methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" ------------------------------------------------------------------------------------------------- """
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/translate", response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest):

    db = get_db()

    task = crud.create_translation_task(db, request.text, request.languages)

    BackgroundTasks.add_task(perform_translation, task.id, request.text, request.languages, db)

    return {"task_id": {task.id}}


""" ------------------------------------------------------------------------------------------------- """

