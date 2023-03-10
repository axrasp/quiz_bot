import logging
import os
import textwrap

import redis
from dotenv import load_dotenv
from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext,
                          CommandHandler, Filters,
                          MessageHandler, Updater)

logger = logging.getLogger('TG_quiz_bot')


def start(update: Update, context: CallbackContext):
    context.user_data['score'] = 0
    context.user_data['questions_qty'] = 0
    reply_keyboard = [['Новый вопрос'], ['Мой счет']]
    update.message.reply_text(textwrap.dedent(
        '''\
        Добро пожаловать в Задавалку!
        Я задаю хитрые вопросы, а ты попробуй на них ответить.
        Приступим?'''),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        ),
    )


def get_question(update: Update, context: CallbackContext):
    db = context.bot_data['database']
    question = db.randomkey()
    answer = db.get(question)

    reply_keyboard = [['Новый вопрос'], ['Мой счет'], ['Сдаться']]
    context.user_data['answer'] = answer.decode()
    context.user_data['questions_qty'] += 1
    update.message.reply_text(
        question.decode(),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


def get_answer(update: Update, context: CallbackContext):
    reply_keyboard = [['Новый вопрос'], ['Мой счет'], ['Сдаться']]
    reply = update.message.text
    if reply in context.user_data['answer']:
        context.user_data['score'] += 1
        update.message.reply_text(
            textwrap.dedent(
                f'''\
                Это верный ответ!
                Верных ответов: {context.user_data["score"]}
                Играем дальше?'''
            ),
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    else:
        update.message.reply_text(
            'Неверный ответ, попробуй еще раз!',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )


def get_score(update: Update, context: CallbackContext):
    reply_keyboard = [['Новый вопрос']]
    update.message.reply_text(
        textwrap.dedent(
            f'''Вопросов задано: {context.user_data["questions_qty"]}
            Верных ответов: {context.user_data["score"]}
            Играем дальше?'''
        ),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        ),
    )


def main():
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    updater = Updater(token)

    logger.setLevel(logging.WARNING)

    redis_db_num = os.getenv('REDIS_DB_NUM')
    redis_db_host = os.getenv('REDIS_DB_HOST')
    redis_db_port = os.getenv('REDIS_DB_PORT')

    db = redis.Redis(
        db=redis_db_num,
        host=redis_db_host,
        port=redis_db_port
    )

    while True:
        try:
            dispatcher = updater.dispatcher

            dispatcher.bot_data['database'] = db

            dispatcher.add_handler(
                CommandHandler('start', start)
            )
            dispatcher.add_handler(
                MessageHandler(Filters.regex('^(Новый вопрос)$'), get_question)
            )
            dispatcher.add_handler(
                MessageHandler(Filters.regex('^(Сдаться)$'), get_question)
            )
            dispatcher.add_handler(
                MessageHandler(Filters.regex('^(Мой счет)$'), get_score)
            )
            dispatcher.add_handler(
                MessageHandler(Filters.text, get_answer)
            )

            updater.start_polling()
            updater.idle()

        except Exception as e:
            logger.error('Возникла ошибка:')
            logger.error(e, exc_info=True)
            logger.warning('Перезапускаю бот')
            continue


if __name__ == "__main__":
    main()
