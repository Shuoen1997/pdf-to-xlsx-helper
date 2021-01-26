from flask import Flask, request, redirect, url_for, flash, render_template, send_file
from flask_uploads import (UploadSet, configure_uploads, IMAGES,
                              UploadNotAllowed)
from Photo import Photo
app = Flask(__name__)
photos = UploadSet('photos', IMAGES)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        global photos
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return None
    if request.method == 'POST' and 'download' in request.form:
        return redirect(url_for('download'))

    return render_template('main.html')

@app.route('/download')
def download():
    print("Downloading...")
    return send_file('pdf_folder/2021012000999.pdf',
                     mimetype='application/pdf',
                     attachment_filename='myPDF.pdf',
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)