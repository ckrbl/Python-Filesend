#!/usr/bin/env python

from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
from werkzeug import run_simple
from os.path import dirname, join
from pathlib import Path

UPLOAD_FOLDER = join(dirname(__file__), 'UPLOADS')
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

MAIN_PAGE = '''<!doctype html>
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


def save_file_to_disk(wkz_file):
    if not wkz_file.filename:
        return False

    sanitized_filename = secure_filename(wkz_file.filename)
    wkz_file.save(join(UPLOAD_FOLDER, sanitized_filename))
    wkz_file.close()
    return True


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    def handle_post():
        # If request did not contain files, do nothing
        if 'file' not in request.files:
            return
        wkz_files = request.files.getlist('file')
        for wkz_file in wkz_files:
            # If file is None, skip it
            if not wkz_file:
                continue

            # If file sent with no path.. quit the whole request
            if not save_file_to_disk(wkz_file):
                return

    if 'POST' == request.method:
        handle_post()
        return redirect(request.url)

    return MAIN_PAGE


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, app)
