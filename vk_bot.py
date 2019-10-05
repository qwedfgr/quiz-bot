import os
import random

import dotenv
import redis
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

import quiz_tools

dotenv.load_dotenv()
QUESTIONS = quiz_tools.get_dict_of_questions()
DB = redis.Redis(host=os.environ['HOST'],
                 password=os.environ['PASSWORD_REDIS'],
                 port=os.environ['PORT'],
                 decode_responses=True, db=0
                 )
TOKEN_VK = os.environ["TOKEN_VK"]


def main():
    run_vk_bot(TOKEN_VK)


def get_answer(event, vk_api):
    if event.text == 'Новый вопрос':
        question = random.choice(list(QUESTIONS.keys()))
        DB.set(event.user_id, question)
        vk_api.messages.send(
            user_id=event.user_id,
            message=f'Вопрос: {question}',
            random_id=random.randint(1, 1000),
            keyboard=get_keyboard()
        )
    elif event.text == 'Сдаться':
        question = DB.get(event.user_id)
        answer = QUESTIONS[question]
        vk_api.messages.send(
            user_id=event.user_id,
            message=f'Ответ: {answer}',
            random_id=random.randint(1, 1000),
            keyboard=get_keyboard()
        )
    else:
        question = DB.get(event.user_id)
        text = event.text
        if QUESTIONS[question] == text:
            vk_api.messages.send(
                user_id=event.user_id,
                message='Правильно!',
                random_id=random.randint(1, 1000),
                keyboard=get_keyboard()
            )
        else:
            vk_api.messages.send(
                user_id=event.user_id,
                message='Неправильно! Попробуйте еще раз.',
                random_id=random.randint(1, 1000),
                keyboard=get_keyboard())


def get_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def run_vk_bot(token_vk):
    vk_session = VkApi(token=token_vk)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_answer(event, vk_api)


if __name__ == '__main__':
    main()
