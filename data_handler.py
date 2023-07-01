import connection
import csv

FILE_QUESTIONS = "sample_data/question.csv"
FILE_ANSWERS = "sample_data/answer.csv"

# FIELD_LABELS defines nice, human-readable labels for data fields
FIELD_LABELS = {
    'questions': {
        'id': 'ID',
        'submission_time': 'Date',
        'view_number': 'Views',
        'vote_number': 'Votes',
        'title': 'Title',
        'message': 'Message',
        'image': 'Image'
    },
    'answers': {
        'id': 'ID',
        'submission_time': 'Date',
        'vote_number': 'Votes',
        'question_id': 'Question ID',
        'message': 'Message',
        'image': 'Image'
    }
}


def get_questions(question_id=None):
    if question_id is None:
        return connection.read_data(FILE_QUESTIONS)
    else:
        questions = connection.read_data(FILE_QUESTIONS)
        return [question for question in questions if str(question['id']) == str(question_id)]


def get_answers(answer_id=None):
    if answer_id is None:
        return connection.read_data(FILE_ANSWERS)
    else:
        answers = connection.read_data(FILE_ANSWERS)
        return [answer for answer in answers if str(answer['id'] == str(answer_id))]


def get_questions_headers():
    return connection.get_csv_fieldnames(FILE_QUESTIONS)


def get_answers_headers():
    return connection.get_csv_fieldnames(FILE_ANSWERS)


def get_question_answers(question_id):
    return [answer for answer in get_answers() if str(answer['question_id']) == str(question_id)]


def save_question(question_data):
    questions = get_questions()
    question_ids = [int(question['id']) for question in questions]
    new_question_id = max(question_ids) + 1
    question_data['id'] = new_question_id
    question_data['vote_number'] = 0
    connection.write_data(FILE_QUESTIONS, question_data)
    return new_question_id


def save_answer(answer_data):
    answers = get_answers()
    answer_ids = [int(answer['id']) for answer in answers]
    new_answer_id = max(answer_ids) + 1
    answer_data['id'] = new_answer_id
    answer_data['vote_number'] = 0  # Dodana linia z 0
    connection.write_data(FILE_ANSWERS, answer_data)
    return new_answer_id


def delete_answer(answer_id):
    answers = get_answers()
    answers = [answer for answer in answers if str(answer['id']) != str(answer_id)]

    with open(FILE_ANSWERS, 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for answer in answers:
            writer.writerow(answer)


def delete_question(question_id):
    questions = get_questions()
    questions = [question for question in questions if str(question['id']) != str(question_id)]

    with open(FILE_QUESTIONS, 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for question in questions:
            writer.writerow(question)


def vote_answer(answer_id, vote_change):
    answers = get_answers()
    for answer in answers:
        if str(answer['id']) == str(answer_id):
            if answer['vote_number'] == '':
                answer['vote_number'] = '0'
            answer['vote_number'] = int(answer['vote_number']) + vote_change
    with open(FILE_ANSWERS, 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for answer in answers:
            writer.writerow(answer)


def vote_question(question_id, vote_change):
    questions = get_questions()
    for question in questions:
        if str(question['id']) == str(question_id):
            question['vote_number'] = int(question['vote_number']) + vote_change
    with open(FILE_QUESTIONS, 'w', newline='') as csvfile:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for question in questions:
            writer.writerow(question)
