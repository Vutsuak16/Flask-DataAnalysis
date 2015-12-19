import os
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import json, json2html

UPLOAD_FOLDER = 'C:\Users\windows 7\Desktop\Flask_Upload'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('analyze'))
    return render_template('gui_data.html')


@app.route("/analyze")
def analyze():
    for file in os.listdir('C:\Users\windows 7\Desktop\Flask_Upload'):
        if file.endswith(".csv"):
            df = pd.read_csv("C:\Users\windows 7\Desktop\Flask_Upload" + "\\" + file,sep=",")
            data = df.describe()
            os.remove("C:\Users\windows 7\Desktop\Flask_Upload" + "\\" + file)
            return data.to_html()
        elif file.endswith(".xlsx") or file.endswith(".xls"):
            df = pd.read_excel("C:\Users\windows 7\Desktop\Flask_Upload" + "\\" + file,sep=",")
            data = df.describe()
            os.remove("C:\Users\windows 7\Desktop\Flask_Upload" + "\\" + file)
            return data.to_html()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
