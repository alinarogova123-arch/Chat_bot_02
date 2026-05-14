# Game of werbs bot

Бот поддержки для ответов на типичные вопросы.

<img width="545" height="600" alt="demo_vk_bot" src="https://github.com/user-attachments/assets/5bebde2b-42d0-479a-9644-084a5aa58177" />

Использует Dialogflow от Google для выбора нужных ответов на поступающие сообщения.

Пример работы бота можно увидеть в группе ВК [https://vk.com/club238671047], написав сообщение в группу.

## Запуск

Для запуска бота у вас уже должен быть установлен Python 3, аккаунт Google, Телеграм бот и группа ВК.

- Скачайте код.
- Создайте проект Google Cloud на [https://console.cloud.google.com/].
- Включите API Dialogflow на вашем гугл аккаунте
- Создайте Dialogflow агента на [https://dialogflow.cloud.google.com/] и укажите ID вашего проекта при создании агента.
- Установите Google Cloud CLI и авторизуйтесь в ней с помощью своего аккаунта Google.
- Запустите команду `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform` для получения json файла доступа.
- Установите зависимости командой `pip3 install -r requirements.txt`
- Задайте переменные окружения.
- Запустите обучение вашего Dialogflow агента командой `add_intent.py`
- Запустите бота для Телеграм командой `python3 TG_bot.py`
- Запустите бота для Вконтакте командой `python3 TG_bot.py`

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом в корневом каталоге проекта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следущие переменные:
- `TELEGRAM_BOT_API_KEY` — Токен телеграм бота.
- `PROGECT_ID` — ID вашего проекта Google Cloud.
- `TELEGRAM_CHAT_ID` — ID вашего чата с ботом.
- `PATH_TO_CREDENTIALS` — Путь к json файлу доступа.
- `VK_API_KEY` — Токен вашего сообщества Вконтакте.
 

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

