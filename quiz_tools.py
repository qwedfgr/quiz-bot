import glob
import os
import re


def get_dict_of_questions():
    directory = 'quiz-questions'
    questions_dict = {}

    for filename in glob.glob(os.path.join(directory, '*.txt')):
        with open(filename, 'r', encoding='KOI8-R') as file_content:
            file_content = file_content.read()
        questions = file_content.split('\n\n\n')
        for question in questions:
            question_and_answer = question.split('\n\n')
            for text in question_and_answer:
                if re.findall('Вопрос.*:', text):
                    question_text = re.split('Вопрос.*:', text)[1]
                    question_text = question_text.replace('\n', ' ')
                if re.findall('Ответ:', text):
                    answer_text = re.split('Ответ:', text)[1]
                    answer_text = answer_text.replace('\n', ' ')
            questions_dict[question_text] = answer_text
    return questions_dict
