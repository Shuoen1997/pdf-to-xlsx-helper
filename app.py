from flask import Flask, request, render_template, send_from_directory, url_for, redirect, flash
import os
from werkzeug.utils import secure_filename
from pdf_convertor import *

app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + '/pdf_folder'
DOWNLOAD_FOLDER = os.getcwd() + '/xlsx_folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)

            extract_PDF_textbox(pdf_name=full_path)
            output_file_name = convert_to_xlsx(pdf_name=filename)
            file.save(output_file_name)
            print(output_file_name)
            try:
                return redirect(url_for('download', filename=output_file_name))
            except Exception:
                abort(404)
    return render_template('index.html')

@app.route('/convert/<filename>')
def convert(filename):


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'],
                               filename=filename,
                               mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    print(UPLOAD_FOLDER)
    print(DOWNLOAD_FOLDER)
    app.run(debug=True)
