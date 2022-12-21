import telebot
from telebot import types
from Tokens import open_weather_token, telebot_token
from threading import Timer
from schedule_functions import get_group_id_by_name, get_schedule_dict_by_id_and_date, lesson_from_dict
from weather_functions import get_weather
from time_functions import get_tomorrow_date, get_today_date, delta_time
from bot_phrases import phrases

group_number = '5030103/10001'

def main():
    global group_number
    global date
    group_id = get_group_id_by_name(group_number)
    if group_id == -1:
        return f'Номер группы указан неверно \U0001F614!!!'
    else:
        schedule_dict = get_schedule_dict_by_id_and_date(group_id, date)
    if schedule_dict == -1:
        return f'Дата указана неверно \U0001F614!!!'
    else:
        schedule = lesson_from_dict(schedule_dict, date)

    return schedule

#Сам бот
if __name__ == '__main__':
    bot = telebot.TeleBot(telebot_token)
    @bot.message_handler(commands=['start'])
    def start(message):
        mess = f'Привет, <i>{message.from_user.first_name}</i>'
        bot.send_message(message.chat.id, mess, parse_mode='html')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        rasp = types.KeyboardButton('Расписание')
        weather = types.KeyboardButton('Погода')
        reminder = types.KeyboardButton('Напоминание')
        morning = types.KeyboardButton('Доброе утро')
        choose_group = types.KeyboardButton('Выбор группы')
        tomorrow = types.KeyboardButton('Что ждет меня завтра')
        markup.add(rasp, weather, reminder, morning, choose_group, tomorrow)
        bot.send_message(message.chat.id, 'Выбери необходимое', reply_markup = markup)

    @bot.message_handler(commands=['help'])
    def help(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        start = types.KeyboardButton('/start')
        markup.add(start)
        bot.send_message(message.chat.id, phrases['help'], reply_markup = markup)

    @bot.message_handler(content_types=['text'])
    def get_user_text(message):
        global date
        global timetable
        message_text = message.text.lower()
        if message_text == 'привет':
            bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
        elif message_text == 'доброе утро':
            bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            city = 'Санкт-Петербург'
            weather = get_weather(city, open_weather_token)
            bot.send_message(message.chat.id, weather, parse_mode='html')
            date = get_today_date()
            timetable = main()
            bot.send_message(message.chat.id, timetable, parse_mode='html')
        elif message_text == 'что ждет меня завтра':
            bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            date = get_tomorrow_date()
            timetable = main()
            bot.send_message(message.chat.id, timetable, parse_mode='html')
        elif message_text == 'расписание':
            msg = bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            bot.register_next_step_handler(msg, bot_schedule)
        elif message_text == 'погода':
            msg = bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            bot.register_next_step_handler(msg, bot_weather)
        elif message_text == 'напоминание':
            msg = bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            bot.register_next_step_handler(msg, remind)
        elif message_text == 'выбор группы':
            msg = bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
            bot.register_next_step_handler(msg, ch_group)
        elif message_text == 'напомни группу':
            bot.send_message(message.chat.id, group_number, parse_mode='html')
        elif message_text == 'создатели':
            bot.send_message(message.chat.id, phrases[f"{message_text}"], parse_mode='html')
        else:
            bot.send_message(message.chat.id, phrases["not_understand"], parse_mode='html')

    def ch_group(message):
        global group_number
        group_number = message.text
        bot.send_message(message.chat.id, f'Запомнил группу:{group_number}', parse_mode='html')

    def bot_weather(message):
        city = message.text.strip()
        weather = get_weather(city, open_weather_token)
        bot.send_message(message.chat.id, weather, parse_mode='html')

    def remind(message):
        global reminder_text
        reminder_text = message.text.strip()
        global mes_rem_id
        mes_rem_id = message.chat.id
        msg1 = bot.send_message(message.chat.id, f'Когда напомнить?\nвведите: год.месяц.число.час.минута (МСК)', parse_mode='html')
        bot.register_next_step_handler(msg1, reminder_t)

    def send_message(reminder_text):
        remind_text = f"Напоминаю \U0001F99D\n{reminder_text}"
        bot.send_message(mes_rem_id, remind_text, parse_mode='html')

    def reminder_t(message):
        reminder_time = message.text.strip()
        if delta_time(reminder_time) != -1:
            timer = Timer(delta_time(reminder_time), send_message, [reminder_text])
            timer.start()
        else:
            bot.send_message(mes_rem_id, f'Ой, дата указана неверно \U0001F614!!!', parse_mode='html')

    def bot_schedule(message):
        global date
        date = message.text
        timetable = main()
        bot.send_message(message.chat.id, timetable, parse_mode='html')

    @bot.message_handler(content_types=['photo'])
    def get_user_photo(message):
        bot.send_message(message.chat.id, 'Классное фото!', parse_mode='html')

    bot.polling(none_stop=True)