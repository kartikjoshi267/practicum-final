from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from functionLibrary import getNumberPlateText

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = [".png", ".webp", ".jpg"]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "sakj"


@app.route('/')
def main():
    return render_template('index.html', name=None)


def allowed_file(filename):
    return ('.' in filename) and ('.'+filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@app.route('/uploads/<name>')
def access_upload(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if (not allowed_file(f.filename)):
            return "File not supported"
        
        f.save(app.config["UPLOAD_FOLDER"]+"/"+secure_filename(f.filename))
        text = getNumberPlateText(app.config["UPLOAD_FOLDER"]+"/"+secure_filename(f.filename))
        return render_template('index.html', name=app.config["UPLOAD_FOLDER"]+"/"+secure_filename(f.filename), text=text)

    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)
