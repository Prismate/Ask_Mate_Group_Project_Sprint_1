import flask
from flask import Flask, render_template, request
from util import sort_data, validate_image
import data_handler
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "./static/images/"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER


@app.route("/")
def main_page():
    return flask.render_template("main_page.html", title='Home')


@app.route("/list")
def list_page():
    questions = data_handler.get_questions()
    fields = data_handler.get_questions_headers()
    if request.args.get('order_by') and request.args.get('order_direction'):
        order_by_key = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        questions = sort_data(questions, order_by_key, order_direction)
        print(questions)
    return flask.render_template("questions.html", questions=questions, fields=fields, title='Questions',
                                 labels=data_handler.FIELD_LABELS['questions'])


@app.route("/question/<question_id>")
def list_question(question_id=None):
    answers = data_handler.get_question_answers(question_id)
    fields = data_handler.get_answers_headers()
    if question_id is not None:
        question = data_handler.get_questions(question_id)
        return flask.render_template("answers.html", answers=answers, fields=fields, title='Answers',
                                     labels=data_handler.FIELD_LABELS['answers'], question=question)
    else:
        return flask.redirect("/")


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return flask.render_template("add_question.html", title='Add question')
    elif request.method == 'POST':
        question_data = dict(request.form)
        uploaded_file = request.files['image']
        question_data['image'] = uploaded_file.filename
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        new_question_id = data_handler.save_question(question_data)
        return flask.redirect(f"/question/{new_question_id}")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        question = data_handler.get_questions(question_id)
        return flask.render_template("add_answer.html", title='Add answer', question=question)
    elif request.method == 'POST':
        answer_data = dict(request.form)
        uploaded_file = request.files['image']
        answer_data['image'] = uploaded_file.filename
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        new_answer_data = data_handler.save_answer(answer_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    data_handler.delete_question(question_id)
    return flask.redirect("/list")


@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    pass


@app.route("/answer/<answer_id>/delete", methods=['POST'])
def delete_answer(answer_id):
    data_handler.delete_answer(answer_id)
    return flask.redirect(flask.request.referrer)


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def question_vote_up(question_id):
    data_handler.vote_question(question_id, 1)
    return flask.redirect(flask.request.referrer)


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def question_vote_down(question_id):
    data_handler.vote_question(question_id, -1)
    return flask.redirect(flask.request.referrer)


@app.route("/answer/<answer_id>/vote-up", methods=['POST'])
def answer_vote_up(answer_id):
    data_handler.vote_answer(answer_id, 1)
    return flask.redirect(flask.request.referrer)


@app.route("/answer/<answer_id>/vote-down", methods=['POST'])
def answer_vote_down(answer_id):
    data_handler.vote_answer(answer_id, -1)
    return flask.redirect(flask.request.referrer)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010)