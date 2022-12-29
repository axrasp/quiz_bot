# Бот - викторина с возможностью загрузить свои вопросы в TG и VK


Бот позволяет организовать викторину и подсчитывает количество верных ответов пользователя

## Установка

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```


### Получение чувствительных данных

Создайте бота в телеграме через [https://t.me/BotFather](https://t.me/BotFather)

Создайте файл ``.env`` и добавьте в него следующие данные вида:

```
TG_TOKEN=5662038928:AAEm652uxCui7HdiuKu7CKl1STF3faKpW3Q
VK_TOKEN="vk1.a.-xrccnJWctU7lAnbe9-Cx43cbBMczQMx-U9L7sWgc5JHIv_MibxSFWpgE-Gkms149mR4tbDJJaJzBZ3oDJQ6Kcu7arg3S17NpSY6MbpKFsVG8UuVP91NRoi8j9ZA0ZoLJnj4Ek0DR0_UUSPJqV-7lIEUxs0z--TjJtigMtbNa87u0KSfqTo6kPShd7k2r-o6jDst0VPNSV
REDIS_DB_NUM=0
REDIS_HOST='localhost'
REDIS_PORT=6379
```

- TG_TOKEN - Токен телеграм-бот, полученный в [BotFather](https://t.me/BotFather)
- VK_TOKEN - [токен](https://vk.com/@articles_vk-token-groups?ysclid=lb26bno4x7379535242) из вашего сообщества VK
- REDIS_DB_NUM - номер вашей базы данных [Redis](https://redis.io)
- REDIS_HOST- хост базы данных [Redis](https://redis.io)
- REDIS_PORT - порт базы данных [Redis](https://redis.io)

### Заполнение базы данных

Запустите [redis](https://redis.io/docs/getting-started/)

Подготовьте ``JSON-файл`` с вопросами и ответами вида:

```json
{
    "Вопрос 1": "Ответ 1",
    "Вопрос 2": "Ответ 2"
}
```

Пример файла есть в репозитории: ``.questions.json``

Для заполнения базы данных, запустите скрипт командой:

```sh
python fillbase.py --file questions.json
```

где  ``question.json`` - путь к файлу с вопросами


## Запуск TG-бота на локальном сервере

Запустите бот командой:

```
python3 bot.py
```

Запусите бота в телегамме ``/start``

## Запуск VK-бота на локальном сервере

Запустите бот командой:

```
python3 vk_bot.py
```

## Деплой на свой сервер

Загрузите репозиторий на сервер (в этом примере грузим в /opt/your_bot_name).
Создайте виртуальное окружение в папке бота:

```commandline
python3 -m venv venv
```

Активируйте виртуальное окружение:

```
source venv/bin/activate
```
Установите зависимости и чувствительные данные (см. раздел Установка)

### Демонизация бота

#### VK
Создайте новый файл в папке ``/etc/systemd/system`` с названием:
``your_bot_name_vk.service`` для VK-бота c таким содержимым:

```
[Service]
ExecStart=/opt/your_bot_name/venv/bin/python3 /opt/your_bot_name/vk_bot.py
Restart=always


[Install]
WantedBy=multi-user.target
```

Добавляем бота в автозагрузку

```commandline
systemctl enable your_bot_name_vk
```

Запускаем бота:

```commandline
systemctl start your_bot_name_vk
```

#### Telegram
Создайте новый файл в папке ``/etc/systemd/system`` с названием:
``your_bot_name_tg.service`` для TG-бота c таким содержимым:

```
[Service]
ExecStart=/opt/your_bot_name/venv/bin/python3 /opt/your_bot_name/tg_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Добавляем бота в автозагрузку

```commandline
systemctl enable your_bot_name_tg
```

Запускаем бота:

```commandline
systemctl start your_bot_name_tg
```

Подробнее о systemd [здесь](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
Туториал [здесь](https://4te.me/post/systemd-unit-ubuntu/)