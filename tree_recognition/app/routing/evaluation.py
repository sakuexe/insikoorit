from typing import Optional
from fastapi import UploadFile, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from glob import glob
import random
import os

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.post("/evaluate")
async def evaluate_tree(request: Request, file: UploadFile | None = None):
    from main import UPLOAD_FOLDER

    if not file:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"code": 400, "message": "The given file has no filename"}
        )

    file_path = os.path.join(UPLOAD_FOLDER, file.filename or "noname.jpeg")

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    except OSError:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"code": 500,
                     "message": "The file could not be saved to the disk"}
        )

    # choose a random training class name
    # this is just for mocking purposes
    folders = glob("../trees_training/originals/*/")
    random_class = os.path.basename(os.path.normpath(random.choice(folders)))

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"type": random_class, "score": random.random()}
    )
