import config
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

bot = telebot.TeleBot(config.token) #должно быть в начале. Вызывает токен
cred = credentials.Certificate('C:/Users/User/Desktop/verta/bot/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vertabot.firebaseio.com/' })

#result = db.reference('/bot/answers/1/email') #указываете ключ, значение которого хотите получить.
#print(result.get())

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Для себя", "Для бизнеса")
    db.reference("/bot/users/"+str(user_id)).update({"current": "category"})
    bot.send_message(user_id,"Отлично! Я тебя ждал. Для чего тебя нужен бот?",reply_markup = user_markup)
    
@bot.message_handler(content_types = ['text', 'contact'])
def start_dialog(message):
    user_id = message.from_user.id
    current = db.reference("/bot/users/"+str(user_id)+"/current").get()
    print(current)
    if current == "category":
        if message.text == "Для себя":
            bot.send_message(user_id,"Окей, круто! А что ваш бот должен уметь делать?")
            db.reference("/bot/users/"+str(user_id)).update({"category": "self"})
            
            db.reference("/bot/users/"+str(user_id)).update({"current": "ability"})
        elif message.text == "Для бизнеса":
            bot.send_message(message.from_user.id,"Чат-бот для бизнеса очень важен. Что он должен уметь делать?")
            db.reference("/bot/users/"+str(user_id)).update({"category": "business"})
            
            db.reference("/bot/users/"+str(user_id)).update({"current": "ability"})
        else:
            bot.send_message(message.from_user.id,"Ошибка! Выберите из перечисленных.")
    elif current == "ability":
        db.reference("/bot/users/"+str(user_id)).update({"ability": message.text})
        key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        contact_key = telebot.types.KeyboardButton(text="Отправить свой номер", request_contact=True)
        key.add(contact_key)
        bot.send_message(message.from_user.id,"Замечательно! Отправь мне свои контакты, чтобы мы смогли с тобой связаться.", reply_markup = key)
        db.reference("/bot/users/"+str(user_id)).update({"current": "contacts"})
    elif current == "contacts":
        category = db.reference("/bot/users/"+str(user_id)+ str("/category")).get()
        ability = db.reference("/bot/users/"+str(user_id)+ "/ability").get()
        print(message)
        user_name = message.from_user.username
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        phone = db.reference("/bot/users/"+str(user_id)).update({"phone": phone_number})
        user = db.reference("/bot/users/"+str(user_id)).update({"user_name": user_name})
        name = db.reference("/bot/users/"+str(user_id)).update({"name": first_name})
        
        bot.send_message(message.from_user.id,"Отлично! В скором времени мы с тобой свяжемся :) Если хочешь можешь вернуться на наш сайт.")
        inline = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text = "Verta", url = "http://bitpine.ru/verta/")
        inline.add(url_button)
        bot.send_message(message.from_user.id,"Ссылка на сайт", reply_markup = inline)
        
        bot.send_message("337465823", "От кого: " + str(first_name) + " @" + str(user_name)  + "\nНомер: " + str(phone_number) +  "\nДля чего: " + category + "\nЧто он должен уметь: " + ability)
        bot.send_message("342420058", "От кого: " + str(first_name) + " @" + str(user_name)  + "\nНомер: " + str(phone_number) +  "\nДля чего: " + category + "\nЧто он должен уметь: " + ability)
    

bot.polling(none_stop=True, interval = 2) #в конце. Бесконечно.


