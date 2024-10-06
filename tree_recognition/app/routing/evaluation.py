from fastapi import UploadFile, File, HTTPException, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from glob import glob
import random
import os

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.post("/evaluate")
async def evaluate_tree(request: Request, file: UploadFile = File(...)):
    from main import UPLOAD_FOLDER

    if not file:
        raise HTTPException(status_code=401, detail="No file was passed")
    if not file.filename:
        raise HTTPException(
            status_code=401, detail="given image had no filename")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # choose a random training class name
    # this is just for mocking purposes
    folders = glob("../trees_training/originals/*/")
    random_class = os.path.basename(os.path.normpath(random.choice(folders)))

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"type": random_class, "score": random.random()}
    )
