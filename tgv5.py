import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Устанавливаем токен бота и API ключ модели ChatGPT
BOT_TOKEN = 'YOUR_BOT_TOKEN'
openai.api_key = 'YOUR_API_KEY'

updater = Updater(token=BOT_TOKEN, use_context=True)
# Функция для генерации ответа на сообщение пользователя
def generate_reply(text):

    prompt = f"User: {text}\nChatGPT: "
    response = openai.Completion.create(engine="gps-3.5-turbo", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.7)
    message = response.choices[0].text.strip()
    return message

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который использует модель ChatGPT для генерации текста. Просто отправь мне сообщение, и я постараюсь на него ответить!")

# Обработчик текстовых сообщений
def message(update, context):
    text = update.message.text
    reply = generate_reply(text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# Создаем объект бота
bot = telegram.Bot(token=BOT_TOKEN)

# Создаем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)

# Добавляем обработчики команд и сообщений в диспетчер
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Запускаем бота
bot.polling(none_stop=True)
