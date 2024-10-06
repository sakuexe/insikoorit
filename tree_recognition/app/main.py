from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Directory where uploaded images will be stored
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home route to render the HTML upload form
@app.get("/", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <head>
            <title>Upload Image</title>
        </head>
        <body>
            <h1>Upload an Image</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """

# Route to handle the image upload
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return RedirectResponse(url=f"/uploads/{file.filename}", status_code=303)
    return {"message": "No file uploaded."}

# Route to display the uploaded image
@app.get("/uploads/{filename}", response_class=HTMLResponse)
async def uploaded_file(filename: str):
    return f"""
    <html>
        <head>
            <title>Uploaded Image</title>
        </head>
        <body>
            <h1>Image successfully uploaded!</h1>
            <img src="/static/uploads/{filename}" alt="{filename}" style="width:200px; margin:10px;">
        </body>
    </html>
    """