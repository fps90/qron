import telebot
from telebot import types

token = "5774874510:AAHeS9R5uYQIYk4u-uFatiilelvBZ_3YMO8"
bot = telebot.TeleBot(token)

# Dictionary to store user IDs with their respective page numbers
user_pages = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, "مرحبا بك {} \n الرجاء ارسال رقم الصفحة لتصفح صفحات القرآن الكريم .".format(name))

@bot.message_handler(regexp=r'^\d+$')
def all(message):
    try:
        num = int(message.text)
        user_pages[message.chat.id] = message.from_user.id  # Store the user ID with the chat ID
        url = "https://quran.ksu.edu.sa/png_big/" + str(num) + ".png"

        keyboard = types.InlineKeyboardMarkup()
        cou = types.InlineKeyboardButton(text=f"• {num} •", callback_data="couu")
        previous = types.InlineKeyboardButton(text="صفحة السابقة", callback_data=str(num - 1))
        next = types.InlineKeyboardButton(text="صفحة التالية", callback_data=str(num + 1))

        keyboard.row(cou)
        keyboard.row(previous, next)

        bot.send_photo(message.chat.id, url, reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, 'حدث خطأ')

@bot.callback_query_handler(func=lambda call: True)
def alll(call):
    if call.data == 'couu':
        bot.answer_callback_query(call.id, text='هذا زر يعرض فيه العدد فقط')
        return
    
    # Check if the user who pressed the button is the same as the one who sent the original message
    if call.from_user.id != user_pages.get(call.message.chat.id):
        bot.answer_callback_query(call.id, text='هذا الأمر لا يخصك.')
        return

    try:
        num = int(call.data)
        url = "https://quran.ksu.edu.sa/png_big/" + str(num) + ".png"

        keyboard = types.InlineKeyboardMarkup()

        cou = types.InlineKeyboardButton(text=f"• {num} •", callback_data="couu")
        previous = types.InlineKeyboardButton(text="صفحة السابقة", callback_data=str(num - 1))
        next = types.InlineKeyboardButton(text="صفحة التالية", callback_data=str(num + 1))

        keyboard.row(cou)
        keyboard.row(previous, next)

        bot.edit_message_media(types.InputMediaPhoto(url), call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(call.message, 'حدث خطأ')

print('run')
bot.infinity_polling()
