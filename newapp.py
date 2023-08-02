# 1. Import necessary modules
import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from gtts import gTTS
from ocr_module import ocr_image

# Set the path to the Tesseract executable (change this if necessary)
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 2. Create an instance of the Flask class
app = Flask(__name__)
global_text = None
# 3. Define a route to handle the main page
@app.route('/')
def index():
    return render_template('testindex1.html')

# 4. Define a route to handle the photo upload
@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'photo' not in request.files:
        return "No file part"
    
    file = request.files['photo']
    
    # Check if the file has a valid filename
    if file.filename == '':
        return "No selected file"
    
    # Check if the file is allowed (optional)
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return "Invalid file type"
    
    # Save the file to a secure location
    base_path = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.join(base_path, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    
    
    #return redirect(url_for('upload_successful'))
 
    # Process the image using OCR
    extracted_text = ocr_image(file_path)

    return redirect(url_for('upload_successful',values=extracted_text))
    
    #return render_template('upload.html', text=extracted_text)

# 5. Define a route to handle the upload success page
@app.route('/upload_successful')
def upload_successful():
    extracted_text = request.args.get('values')
    return render_template('testupload1.html', text=extracted_text)

@app.route('/speech_generation')
def speech_generation():
    extracted_text = request.args.get('extracted_text', '')
    tts = gTTS(text=extracted_text, lang='en')

    base_path = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.join(base_path, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
     
    audio_file = os.path.join(upload_folder, 'output.mp3')
    tts.save(audio_file)

    return render_template('testaudio1.html', audio_file=audio_file)

@app.route('/download')
def download():
    audio_file = request.args.get('file')
    return send_file(audio_file, as_attachment=True)

@app.route('/about')
def about():
    return render_template('testabout1.html')

if __name__ == '__main__':
    app.run(debug=True)
