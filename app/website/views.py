from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, send_from_directory, flash
from werkzeug.utils import secure_filename
from .utilities.file_operations import allowed_file
import os
from .txt2tei.file_load import load_txt_file_to_string
from .txt2tei.parser import parser
from .txt2tei.md_finders import find_tags_in_text
from .txt2tei.replace_md_tei import replace_tags

views = Blueprint("views", __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("load-file.html")
    elif request.method == 'POST':
        UPLOAD_FOLDER = 'uploads'
        ALLOWED_EXTENSIONS = {'txt', 'md'}
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('views.home'))
        file = request.files['file']
        if file.filename == "":
            flash('no selected file')
            return redirect(url_for('views.home'))
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(views.root_path, UPLOAD_FOLDER, filename))
            session['text'] = (UPLOAD_FOLDER, filename)
            session.modified = True
            return redirect(url_for('views.file_parser'))

@views.route('/file-parser', methods=['GET'])
def file_parser():
    if session.get('text') is None:
        return redirect(url_for('views.home'))
    else:
        text = load_txt_file_to_string(os.path.join(views.root_path, session['text'][0], session['text'][1]))
        valid_tags, tokenized_text, error_list, errors = parser(text)
        if errors == False:
            converted_text = replace_tags(valid_tags, tokenized_text)
        return render_template('file-parser.html', text = text, errors_exist = errors, error_list = error_list, converted_text = converted_text)


@views.route('/logout', methods=['GET'])
def logout():
    session.pop('text', None)
    return redirect(url_for('views.home'))