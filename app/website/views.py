from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, send_from_directory, flash, current_app
from werkzeug.utils import secure_filename
from .utilities.file_operations import allowed_file
from .utilities.text_manipulation import remove_tags
from .utilities.text_manipulation import remove_empty_tags
import os
from .txt2tei.file_load import load_txt_file_to_string
from .txt2tei.file_load import html_safe
from .txt2tei.parser import parser
from .txt2tei.md_finders import find_tags_in_text
from .txt2tei.replace_md_tei import replace_tags
from .txt2tei.replace_md_tei import add_outer_tags
from .txt2tei.errors import mark_errors_for_display

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

@views.route('/file-parser', methods=['GET', 'POST'])
def file_parser():
    # If no text has been uploaded text
    if session.get('text') is None:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'GET':
            # If the file has been uploaded now
            text = load_txt_file_to_string(os.path.join(views.root_path, session['text'][0], session['text'][1]))
            # the inclusion of '<' and '>' is playing havoc with the text, so we'll add a space to them, to prevent them from being renedered by the browser
            text = html_safe(text)
        elif request.method == 'POST':
            # if it's the result of the update button
            text = request.form["text"]
            text = remove_tags(text)

        # parse the text
        valid_tags, tokenized_text, error_list, errors = parser(text)

        if errors == False:
            # changes internal tags
            tokenized_text = replace_tags(valid_tags, tokenized_text)
            # adds paragraphs
            tokenized_text = add_outer_tags(tokenized_text)
            # joins tokens for display
            converted_text = "".join(tokenized_text[:])
            # Cleans empty p tags
            converted_text = remove_empty_tags(converted_text)
        else:
            converted_text = False
            text = "".join(mark_errors_for_display(error_list, tokenized_text))
        return render_template('file-parser.html', text = text, errors_exist = errors, error_list = error_list, converted_text = converted_text)

@views.route('/test', methods=['GET', 'POST'])
def test():
    text = load_txt_file_to_string(os.path.join(views.root_path, session['text'][0], session['text'][1]))
    # print(text[80000:])
    return text;

@views.route('/logout', methods=['GET'])
def logout():
    session.pop('text', None)
    return redirect(url_for('views.home'))