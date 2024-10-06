from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Directory where uploaded images will be stored
UPLOAD_FOLDER = 'tree_recognition/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Home route to render the HTML upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')


# Route to handle the image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('uploaded_file', filename=file.filename))

# Route to display the uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'Image successfully uploaded! <br><img src="{url_for("static", filename="uploads/" + filename)}">'


if __name__ == "__main__":
    app.run(debug=True)