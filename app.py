from flask import Flask, request, render_template, send_from_directory, url_for, redirect, flash
import os
from werkzeug.utils import secure_filename
from pdf_convertor import *

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = os.getcwd() + '/pdf_folder'
DOWNLOAD_FOLDER = os.getcwd() + '/xlsx_folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['ALLOWED_FILE_TYPE'] = ['PDF']
app.secret_key = 'asfjdijawpeiftt'


def is_allowed_file_type(filename):
    file_extension = filename.split('.')[-1].upper()
    return file_extension in app.config['ALLOWED_FILE_TYPE']


upload_filename_full = ''
output_filename = ''


@app.route('/', methods=['POST', 'GET'])
def upload_file():
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
            global upload_filename_full
            upload_filename_full = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
            file.save(upload_filename_full)
            flash(f'SUCCESS! {file.filename} is uploaded')
            return render_template('index.html')

    return render_template('index.html')


@app.route('/convert/', methods=['POST', 'GET'])
def convert_file():
    if request.method == 'POST':
        global upload_filename_full
        global output_filename
        if not upload_filename_full:
            return render_template('index.html', convert_message='File not found')
        text_success_message = extract_PDF_textbox(pdf_name=upload_filename_full)
        output_filename = convert_to_xlsx(pdf_name=upload_filename_full)
        convert_message = f'{text_success_message}! {output_filename} generated'
        return render_template('index.html', convert_message=convert_message)

    return redirect(url_for('upload_file'))


@app.route('/download/', methods=['POST', 'GET'])
def download_file():
    global output_filename
    if request.method == 'POST':
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
        global output_filename
        global upload_filename_full
        output_filename = ''
        upload_filename_full = ''
        for pdf_file in os.listdir(app.config['UPLOAD_FOLDER']):
            print(pdf_file)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], pdf_file))
        for xlsx_file in os.listdir(app.config['DOWNLOAD_FOLDER']):
            print(xlsx_file)
            os.remove(os.path.join(app.config['DOWNLOAD_FOLDER'], xlsx_file))
        return redirect(url_for('upload_file'))
    return redirect(url_for('upload_file'))


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    print(UPLOAD_FOLDER)
    print(DOWNLOAD_FOLDER)
    app.run(debug=True)
