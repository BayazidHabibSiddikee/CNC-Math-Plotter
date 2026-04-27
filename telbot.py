API = "8690254124:AAG4hFS89yHbsEcNT3Wsfoa6io1jlVUAGgI" #API key for tel bot

import telebot
bot = telebot.TeleBot(token=API)

@bot.message_handler(commands=['draw'])
def welcome(message):
    bot.send_message(message.chat.id,f"Welcome {message.from_user.first_name}")
    if "draw" in message.text:
        msg = message.text.lower()
        print(msg)
        bot.register_next_step_handler(message, funs)

def funs(message):
    name = message.text.lower()
    if name=="circle":
        from new import Draw
        b = Draw(0,5,13)
        b.circle()
    print(name)

bot.polling()