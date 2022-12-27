import logging
import os

import redis
from dotenv import load_dotenv
from telegram import (ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext,
                          CommandHandler, Filters,
                          MessageHandler, Updater)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('TG_quiz_bot')


def start(update: Update, context: CallbackContext):
    context.user_data['score'] = 0
    context.user_data['questions_qty'] = 0
    reply_keyboard = [['Новый вопрос'], ['Мой счет']]
    update.message.reply_text(
        'Добро пожаловать в Задавалку!\n'
        'Я задаю хитрые вопросы, а ты попробуй на них ответить.\n\n'
        'Приступим?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )


def get_question(update: Update, context: CallbackContext):
    redis_db_num = os.getenv('REDIS_DB_NUM')
    r = redis.Redis(db=redis_db_num)
    question = r.randomkey()
    answer = r.get(question)

    reply_keyboard = [['Новый вопрос'], ['Мой счет'], ['Сдаться']]
    context.user_data['answer'] = answer.decode()
    context.user_data['questions_qty'] += 1
    update.message.reply_text(
        question.decode(),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True
            )
    )


def get_answer(update: Update, context: CallbackContext):
    reply_keyboard = [['Новый вопрос'], ['Мой счет'], ['Сдаться']]
    reply = update.message.text
    if reply in context.user_data['answer']:
        context.user_data['score'] += 1
        update.message.reply_text(
            'Это верный ответ!\n\n'
            f'Верных ответов: {context.user_data["score"]}'
            'Играем дальше?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True
            )
        )
    else:
        update.message.reply_text(
            'Неверный ответ, попробуй еще раз!',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True
            )
        )


def get_score(update: Update, context: CallbackContext):
    reply_keyboard = [['Новый вопрос']]
    update.message.reply_text(
        f'Вопросов задано: {context.user_data["questions_qty"]}\n'
        f'Верных ответов: {context.user_data["score"]}\n\n\n'
        'Играем дальше?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )


def main():
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    updater = Updater(token)
    while True:
        try:
            dispatcher = updater.dispatcher
            dispatcher.add_handler(
                CommandHandler("start", start)
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
