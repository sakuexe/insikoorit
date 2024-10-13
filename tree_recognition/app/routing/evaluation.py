from fastapi import UploadFile, Request
from fastapi import APIRouter
from fastapi.applications import FastAPI
from fastapi.templating import Jinja2Templates
from torch.nn import Module
from contextlib import asynccontextmanager
import asyncio
import os
# local
from single_image_inteference import InferenceResult, generate_infer
from model_state import load_entire_model

templates = Jinja2Templates(directory="templates")

model: Module | None = None


async def load_model():
    global model
    model = await load_entire_model("the_best_one.pth")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """load the model asynchronously in the background
    when the app is started. this way it will only be loaded once
    while still keeping the web app responsive."""
    asyncio.create_task(load_model())
    yield
    # this is ran when the app is shutting down
    model = None


router = APIRouter(lifespan=lifespan)


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
            context={
                "code": 500,
                "message": "The file could not be saved to the disk"
            }
        )

    if not model:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "code": 503,
                "message": "The model is still loading, try again in a moment"
            }
        )

    infer_result: InferenceResult = generate_infer(
        model,
        image_path=file_path,
    )

    # after the model has done its work, remove the saved image
    asyncio.create_task(remove_file_async(file_path))

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "type": infer_result.prediction,
            "score": infer_result.confidence,
            "probabilities": infer_result.probabilities
        }
    )


async def remove_file_async(file_path: str):
    """Asynchronously remove the file."""
    try:
        os.remove(file_path)
    except OSError as err:
        print(f"Error while removing file from: {file_path}")
        print(err)
