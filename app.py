from flask import Flask, request, render_template, send_from_directory, url_for, redirect, flash, current_app
import os
from werkzeug.utils import secure_filename
from pdf_convertor import *


def create_app():
    app = Flask(__name__, template_folder='templates')
    UPLOAD_FOLDER = os.getcwd() + '/pdf_folder'
    DOWNLOAD_FOLDER = os.getcwd() + '/xlsx_folder'

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
    app.config['ALLOWED_FILE_TYPE'] = ['PDF']
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'asfjdijawpeiftt'
    app.config['UPLOAD_FILENAME'] = None
    app.config['OUTPUT_FILENAME'] = None
    return app


app = create_app()


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    def is_allowed_file_type(filename):
        """
        We check to make sure the uploaded file is PDF
        """
        file_extension = filename.split('.')[-1].upper()
        return file_extension in app.config['ALLOWED_FILE_TYPE']

    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('PLEASE UPLOAD A FILE!')
            return redirect(url_for('upload_file'))

        if not is_allowed_file_type(file.filename):
            flash('PLEASE UPLOAD PDF FILE ONLY')
            return redirect(url_for('upload_file'))

        if file:
            upload_filename = secure_filename(file.filename)
            app.config['UPLOAD_FILENAME'] = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
            file.save(app.config['UPLOAD_FILENAME'])
            flash(f'SUCCESS! {file.filename} is uploaded')
            return render_template('index.html')

    return render_template('index.html')


@app.route('/convert/', methods=['POST', 'GET'])
def convert_file():
    if request.method == 'POST':
        if not app.config['UPLOAD_FILENAME']:
            return render_template('index.html', convert_message='File not found')
        text_success_message = extract_PDF_textbox(pdf_name=upload_filename_full)
        app.config['OUTPUT_FILENAME'] = convert_to_xlsx(pdf_name=upload_filename_full)
        convert_message = f'{text_success_message}! {output_filename} generated'
        return render_template('index.html', convert_message=convert_message)

    return redirect(url_for('upload_file'))


@app.route('/download/', methods=['POST', 'GET'])
def download_file():
    if request.method == 'POST':
        output_filename = app.config['OUTPUT_FILENAME']
        if not output_filename:
            return render_template('index.html', download_message='File does not exit, cannot download')
        return send_from_directory(app.config['DOWNLOAD_FOLDER'],
                                   filename=output_filename,
                                   as_attachment=True,
                                   mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    return redirect(url_for('upload_file'))


@app.route('/clear/', methods=['POST'])
def clear():
    if request.method == 'POST':
        # Reset these values and clear the folders to give a clean start
        app.config['OUTPUT_FILENAME'] = None
        app.config['UPLOAD_FILENAME'] = None
        for pdf_file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pdf_file))
        for xlsx_file in os.listdir(app.config['DOWNLOAD_FOLDER']):
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], xlsx_file))
        return redirect(url_for('upload_file'))
    return redirect(url_for('upload_file'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
