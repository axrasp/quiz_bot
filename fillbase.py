import argparse
import json
import os

import redis
from dotenv import load_dotenv


def fill_base(file, redis_db_num, redis_port, redis_host):
    r = redis.Redis(
        db=redis_db_num,
        port=redis_port,
        host=redis_host
    )
    with open(file, 'r') as f:
        quiz = json.load(f)
    for question, answer in quiz.items():
        r.mset({question: answer})
    r.bgsave()


def main():
    load_dotenv()
    redis_db_num = os.getenv('REDIS_DB_NUM')
    redis_port = os.getenv('REDIS_DB_PORT')
    redis_host = os.getenv('REDIS_DB_HOST')

    parser = argparse.ArgumentParser(
        prog='Quiz Bot',
        description='Задаватель вопросов')
    parser.add_argument('--file',
                        help='Заполнение базы вопросами из JSON Файла'
                             '--file filename.json',
                        required=False)
    args = parser.parse_args()

    if args.file:
        fill_base(args.file, redis_db_num, redis_port, redis_host)


if __name__ == '__main__':
    main()
