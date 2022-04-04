import telebot
import pandas as pd
from telebot import types
from token_key import TOKEN  # this line code is used to import private token key
import parse


BOT_TEXT = """Меня зовут Jarvis! Я выполняю парсинг c сайта avito.ru.\n
Введите интересующее Вас объявление, а я соберу для Вас данные и выведу результат в виде таблицы и графиков."""


bot = telebot.TeleBot(TOKEN)


def check_parse_command(text):
    return text.split()[0] == '/parse'


def extract_request(text):
    return ' '.join(text.split()[1:]) if len(text.split()) > 1 else None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = f"Добро пожаловать, {message.chat.username}!\n" + BOT_TEXT
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Парсинг объявления")
    btn2 = types.KeyboardButton("Помощь / help")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    text = f"/start - Начальное меню\n" \
           f"/parse * - парсинг введенного объявления,\n" \
           f"вместо символа '*' введите объявление"
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(content_types=['text'])
def just_do_it(message):
    if message.text == 'Помощь / help':
        send_help(message)
    elif message.text == 'Парсинг объявления' or message.text == '/parse':
        markup = types.ForceReply(input_field_placeholder='/parse kio rio 2015')
        bot.send_message(message.chat.id, 'ВВедите объявление для парсинга: ', reply_markup=markup)
    elif check_parse_command(message.text) and extract_request(message.text) is not None:
        r_text = extract_request(message.text)
        parse.df_dict = parse.to_parse(r_text, parse.df_dict)
        state_file, file_dir, response = parse.save_to_excel(r_text, parse.df_dict)
        info = pd.DataFrame(parse.df_dict)
        bot.send_message(message.chat.id, text=str(info.describe()))
        state_img, img_dir = parse.save_img_res(r_text, parse.df_dict)
        # открывается графическое представление парсинга
        with open(img_dir, 'rb') as img_data:
            bot.send_photo(message.chat.id, img_data)
        # файл  xlsx для скачивания
        if state_file != 1:
            bot.send_message(message.chat.id, response + '\nГотов к скачиванию')
        else:
            bot.send_message(message.chat.id, 'Запрос ранее происходил. Файл готов к скачиванию')
        with open(file_dir, 'rb') as data:
            bot.send_document(message.chat.id, data)
    else:
        bot.reply_to(message, 'Я не понимаю, что ты хочешь... Помощь /help')




bot.infinity_polling()
