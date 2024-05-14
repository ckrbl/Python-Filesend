#!/usr/bin/env python

import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from os.path import dirname, join
 
UPLOAD_FOLDER = join(dirname(__file__), 'UPLOADS')
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
app = Flask(__name__)
app.secret_key = 'test?!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return True
    #return '.' in filename and \
    #       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def show_page():
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file multiple>
            <input type=submit value=Upload>
        </form>
        '''

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
    return show_page()
