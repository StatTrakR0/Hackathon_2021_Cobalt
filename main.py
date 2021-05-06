from telebot import types
import telebot


bot = telebot.TeleBot('1817845833:AAHx0icJfYu9-TUnoN6pYG0uU7_dnl2nAWQ')
user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None
        self.education = None
        self.skills = None
        self.personality = None
        self.add_info = None
        self.salary = None
        self.profession = None
        self.telephone = None


@bot.message_handler(commands=['resume'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Введіть ваш ПІБ:
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Скільки вам років?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Вік повинен бути числом. Скільки вам років?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Чоловік', 'Жінка')
        msg = bot.reply_to(message, 'Яка у вас стать?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Чоловік') or (sex == u'Жінка'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        msg = bot.reply_to(message, 'Яка у вас освіта?')
        bot.register_next_step_handler(msg, process_education_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_education_step(message):
    try:
        chat_id = message.chat.id
        education = message.text
        user = user_dict[chat_id]
        user.education = education
        msg = bot.reply_to(message, 'Які у вас професійні навички?')
        bot.register_next_step_handler(msg, process_skills_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_skills_step(message):
    try:
        chat_id = message.chat.id
        skills = message.text
        user = user_dict[chat_id]
        user.skills = skills
        msg = bot.reply_to(message, 'Які у вас особисті якості?')
        bot.register_next_step_handler(msg, process_personality_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_personality_step(message):
    try:
        chat_id = message.chat.id
        personality = message.text
        user = user_dict[chat_id]
        user.personality = personality
        msg = bot.reply_to(message, 'Чи є у вас додаткова інформація?')
        bot.register_next_step_handler(msg, process_add_info_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_add_info_step(message):
    try:
        chat_id = message.chat.id
        add_info = message.text
        user = user_dict[chat_id]
        user.add_info = add_info
        msg = bot.reply_to(message, 'На яку заробітню плату ви очікуєте?')
        bot.register_next_step_handler(msg, process_salary_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_salary_step(message):
    try:
        chat_id = message.chat.id
        salary = message.text
        user = user_dict[chat_id]
        user.salary = salary
        msg = bot.reply_to(message, 'Який у вас вид зайнятості?')
        bot.register_next_step_handler(msg, process_profession_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_profession_step(message):
    try:
        chat_id = message.chat.id
        profession = message.text
        user = user_dict[chat_id]
        user.profession = profession
        msg = bot.reply_to(message, 'Вкажіть ваш номер телефону')
        bot.register_next_step_handler(msg, process_telephone_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_telephone_step(message):
    try:
        chat_id = message.chat.id
        telephone = message.text
        user = user_dict[chat_id]
        user.telephone = telephone
        bot.send_message(chat_id, 'Ви успішно зареєструвались ' + user.name + '\nВік:' + str(user.age) + '\nСтать:' + user.sex +
                         '\nОсвіта:' + user.education + '\nПрофесійні навички:' + user.skills +
                         '\nДосвід роботи:' + user.personality + '\nДодаткова інформація:' + user.add_info
                         + '\nОчікувана заробітн плата:' + user.salary + '\nСпеціальність:' + user.profession + '\nТелефон:' + user.telephone)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['start'])
def default_test(message):
    bot.send_message(message.chat.id, "Привіт, я КобальтБот! Я допоможу знайти тобі роботу або робітників."
                                      "Введи /help для відображення команд.")


@bot.message_handler(commands=['help'])
def help_func(message):
    keyboard = types.InlineKeyboardMarkup()
    resume_button = types.InlineKeyboardButton(text="Відправити резюме", callback_data='resume')
    find_job_button = types.InlineKeyboardButton(text="Знайти вакансію", callback_data='get-Vacancion')
    keyboard.add(resume_button, find_job_button)
    bot.send_message(message.chat.id, "Ось команди, які тобі допоможуть:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data == 'resume':
       send_welcome(query.message)
   if data.startswith('get-'):
       bot.send_message(query.message.chat.id, "Зараз поки немає вакансій!")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
bot.polling()
