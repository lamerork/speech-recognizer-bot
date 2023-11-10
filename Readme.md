# Бот распознавания речи в Telegram и VK

Бот для Telegram и VK, отвечающий на самые распространенные вопросы пользователей. Поддерживает Dialogflow

## Как установить

- Предварительно должен быть установлен Python 3.10.
- Для установки зависимостей, используйте команду `pip` (или `pip3`, если есть конфликт с `Python2`) :
- ```pip install -r requirements.txt```
- Необходимо зарегистрировать бота и получить его API-токен

### Переменные окружения
Часть настроек проекта берётся из переменных окружения.
Чтобы их определить, создайте файл `.env` в корневой папке и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`:

- `TELEGRAM_TOKEN` - токен для Telegram-бота, полученный от @BotFather.
- `TELEGRAM_CHAT_ID` -  id чата, куда будут отправляться логи (можно узнать у @userinfobot).
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу json с секретным ключом, ([документация](https://cloud.google.com/docs/authentication/client-libraries))
- `GOOGLE_PRODJECT_ID` - идентификатор проекта в DialogFlow ([документация](https://cloud.google.com/dialogflow/es/docs/quick/setup))
- `VK_TOKEN_GROUP ` - ключ группы VK ([документация](https://vk.com/dev/implicit_flow_user))

## Как запустить

### Запуск бота в Telegram

```bash
python telegram_bot.py
```

### Запуск бота в VK

```bash
python vk_bot.py
```

### Обучение бота Dialogflow

```bash
python dialogflow.py --json 'Путь к файлу в формате JSON'
```
или
```bash
python dialogflow.py --link 'Ссылка на файл в формате JSON'
```

#### Пример файла JSON

```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    ...
}
```

## Пример работы

### Telegram
![telegram-bot](https://github.com/lamerork/speech-recognizer-bot/assets/65411132/e9fb0b81-4d31-4118-a553-a684e22be111)
### Vkontakte
![vk-bot](https://github.com/lamerork/speech-recognizer-bot/assets/65411132/6d100508-5036-41cd-86fe-1d789f82e7bd)


## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
