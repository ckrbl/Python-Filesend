#!/usr/bin/env python

import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug import run_simple
from os.path import dirname, join
 
UPLOAD_FOLDER = join(dirname(__file__), 'UPLOADS')
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PAGE_HTML='''<!doctype html>
<head></head>
<body><center>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<p><input type=file name=file multiple>
    <input type=submit value=Upload>
</form>
</center></body>
'''

def main_page():
    return PAGE_HTML

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if 'POST' == request.method:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        usr_files = request.files.getlist('file')
        for one_file in usr_files:
            # if user does not select file, browser also
            # submit a empty part without filename
            if not one_file:
                continue
            if one_file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            filename = secure_filename(one_file.filename)
            one_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            one_file.close()
    return main_page()

if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, app)
