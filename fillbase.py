import argparse
import json
import os

import redis
from dotenv import load_dotenv


def fill_base(file, redis_db_num):
    r = redis.Redis(db=redis_db_num)
    with open(file, 'r') as f:
        quiz = json.load(f)
    for question, answer in quiz.items():
        print(question)
        r.mset({question: answer})
    r.bgsave()


def main():
    load_dotenv()
    redis_db_num = os.getenv('REDIS_DB_NUM')
    parser = argparse.ArgumentParser(
        prog='Quiz Bot',
        description='Задаватель вопросов')
    parser.add_argument('--file',
                        help='Заполнение базы вопросами из JSON Файла'
                             '--file filename.json',
                        required=False)
    args = parser.parse_args()

    if args.file:
        fill_base(args.file, redis_db_num)


if __name__ == '__main__':
    main()
