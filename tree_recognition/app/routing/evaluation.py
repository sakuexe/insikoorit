from fastapi import UploadFile, Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from glob import glob
from time import sleep
import asyncio
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

    # fake delay
    await asyncio.sleep(0.5)

    # choose a random training class name
    # this is just for mocking purposes
    folders = glob(os.path.join("..", "trees_training", "originals", "*"))
    if len(folders) == 0:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"code": 500,
                     "message": "No folders could be found at \
                     ../trees_training/originals"}
        )
    random_class = os.path.basename(os.path.normpath(random.choice(folders)))

    # after the model has done its work, remove the saved image
    asyncio.create_task(remove_file_async(file_path))

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"type": random_class, "score": random.random()}
    )


async def remove_file_async(file_path: str):
    """Asynchronously remove the file."""
    try:
        os.remove(file_path)
    except OSError as err:
        print(f"Error while removing file from: {file_path}")
        print(err)
