import logging
import os

import vk_api as vk
import redis
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id


logger = logging.getLogger('VK_quiz_bot')


def get_question(event, vk):
    redis_db_num = os.getenv('REDIS_DB_NUM')
    r = redis.Redis(db=redis_db_num)
    question = r.randomkey()
    answer = r.get(question)

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=question.decode()
    )
    return answer.decode()


def get_right_answer(event, vk):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Это правильный ответ!\n\n '
                'Играем еще?'
    )


def get_wrong_answer(event, vk):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message='Неверный ответ\n\n '
                'Попытайся еще!'
    )


def get_score(event, vk, score, question_qty):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=f'Вопросов задано: {question_qty}\n'
                f'Верных ответов: {score}\n\n\n'
                'Играем дальше?',
    )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')

    logger.setLevel(logging.WARNING)

    while True:
        try:
            vk_session = vk.VkApi(token=vk_token)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)

            score = 0
            question_qty = 0
            answer = ''

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text == "Сдаться" or event.text == "Новый вопрос":
                        question_qty += 1
                        answer = get_question(event, vk_api)
                        continue
                    if event.text in answer:
                        score += 1
                        get_right_answer(event, vk_api)
                        continue
                    if event.text == "Мой счет":
                        get_score(event, vk_api, score, question_qty)
                        continue
                    else:
                        get_wrong_answer(event, vk_api)
                        continue

        except Exception as e:
            logger.error('в ВК боте возникла ошибка: ')
            logger.error(e, exc_info=True)
            logger.warning('Перезапускаю бот')
            continue


if __name__ == "__main__":
    main()
