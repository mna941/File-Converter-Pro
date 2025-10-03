from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from converters import document_tools  # your conversion module

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure upload and download folders
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DOWNLOAD_FOLDER'] = 'downloads/'

# Make sure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)


@app.route('/pdf-to-word', methods=['GET', 'POST'])
def pdf_to_word():
    if request.method == 'POST':
        file = request.files.get('file')

        # Check if file is valid
        if not file or not file.filename.lower().endswith('.pdf'):
            flash('Please upload a valid PDF file.')
            return redirect(request.url)

        # Generate unique file name
        uid = str(uuid.uuid4())
        filename = secure_filename(f'{uid}.pdf')
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        try:
            # Convert PDF → DOCX
            out_path = document_tools.pdf_to_docx(upload_path, app.config['DOWNLOAD_FOLDER'], uid)
            out_id = os.path.basename(out_path)

            # Provide download link
            return render_template('pdf_to_word.html',
                                   download_link=url_for('download_file', file_id=out_id))
        except Exception as e:
            flash(f'Conversion failed: {e}')
            return redirect(request.url)

    return render_template('pdf_to_word.html')


@app.route('/download/<file_id>')
def download_file(file_id):
    """Serve converted files as raw downloads."""
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],
                               file_id,
                               as_attachment=True)


# Serve static files
@app.route('/tools/<path:filename>')
def serve_tools(filename):
    return send_from_directory('tools', filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about/index.html')

@app.route('/privacy/')
def privacy():
    return render_template('privacy/index.html')

@app.route('/terms/')
def terms():
    return render_template('terms/index.html')

@app.route('/contact/')
def contact():
    return render_template('contact/index.html')


# Categories
@app.route('/document-category/')
def document_category():
    return render_template('document-category/index.html')

@app.route('/image-category/')
def image_category():
    return render_template('image-category/index.html')

@app.route('/video-category/')
def video_category():
    return render_template('video-category/index.html')

@app.route('/audio-category/')
def audio_category():
    return render_template('audio-category/index.html')

@app.route('/spreadsheet-category/')
def spreadsheet_category():
    return render_template('spreadsheet-category/index.html')

@app.route('/archive-category/')
def archive_category():
    return render_template('archive-category/index.html')

@app.route('/PDF-Converters/')
def pdf_converters():
    return render_template('PDF-Converters/index.html')

@app.route('/JPG-to-PNG/')
def jpg_to_png():
    return render_template('JPG-to-PNG/index.html')

@app.route('/Online-Converters/')
def online_converters():
    return render_template('Online-Converters/index.html')

@app.route('/Audio-&-Video-Tools/')
def audio_video_tools():
    return render_template('Audio-&-Video-Tools/index.html')

@app.route('/Privacy-&-Security/')
def privacy_security():
    return render_template('Privacy-&-Security/index.html')


if __name__ == '__main__':
    app.run(debug=True)
