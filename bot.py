import requests
import telebot
from telebot import types


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Начать")
    markup.add(btn)
    return markup


def get_question():
    response = requests.get("http://jservice.io/api/random")
    question = response.json()[0]["question"]
    answer = response.json()[0]["answer"]
    return question, answer


API_KEY = "6242512235:AAGZ5uSmmbhrO7oMA5k10WHsGH0d8hoilQU"
bot = telebot.TeleBot(API_KEY, parse_mode='markdownv2')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, нажми на кнопку начать чтобы запустить викторину", reply_markup=start_menu())


@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text.lower() == "начать":
        question = get_question()
        a = bot.send_message(message.chat.id, f"Вопрос 1/5:\n{question[0]}")
        print(question[1])
        #bot.send_message(message.chat.id, f"Ответ: ||{question[1]}||")
        bot.register_next_step_handler(a, next_question, question[1], 1, 0, 0)


def next_question(message, ans, n, right, wrong):
    if message.text.lower() == ans.lower():
        bot.send_message(message.chat.id, "Верно")
        right += 1
    else:
        wrong += 1
        bot.send_message(message.chat.id, "Неверно")

    n += 1
    if n < 6:
        question = get_question()
        a = bot.send_message(message.chat.id, f"Вопрос {n}/5:\n{question[0]}")
        print(question[1])
        #bot.send_message(message.chat.id, f"Ответ: ||{question[1]}||")
        bot.register_next_step_handler(a, next_question, question[1], n, right, wrong)
    else:
        bot.send_message(message.chat.id,
                         f"Викторина завершилась\n"
                         f"У вас {right} правильных и {wrong} неправильных ответов", reply_markup=start_menu())


bot.polling(none_stop=True)

