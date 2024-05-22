import telebot
import re
from telebot import types
from enum import Enum
from numbers_api import NumbersApi
from translator import translate


class Commands(Enum):
    TRIVIA = "Получить обычный факт"
    MATH = "Получить математический факт"
    DATE = "Получить факт по дате"
    YEAR = "Получить факт по году"
    KEYBOARD_TEXT = "Выберите категорию фактов"


class StartBot:
    def __init__(self, bot):
        self.bot = bot

        @self.bot.message_handler(commands=["start", "help"])
        def start_help_handler(message):
            self.make_keyboard(message, text=Commands.KEYBOARD_TEXT.value)

    def make_keyboard(self, message, text):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        trivia_button = types.InlineKeyboardButton(Commands.TRIVIA.value, callback_data="trivia")
        math_button = types.InlineKeyboardButton(Commands.MATH.value, callback_data="math")
        date_button = types.InlineKeyboardButton(Commands.DATE.value, callback_data="date")
        year_button = types.InlineKeyboardButton(Commands.YEAR.value, callback_data="year")
        keyboard.add(trivia_button, math_button, date_button, year_button)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)


class ButtonsHandler(StartBot):
    def __init__(self, bot):
        super().__init__(bot)
        self.api = NumbersApi()

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query_handler(call):
            callback_data = call.data
            if callback_data == "trivia":
                answer = self.bot.send_message(call.message.chat.id,
                                               "Введите число, о котором нужен факт, или любое слово "
                                               "для получения факта о случайном числе")
                self.bot.register_next_step_handler(answer, self.create_trivia_fact)
            elif callback_data == "math":
                answer = self.bot.send_message(call.message.chat.id,
                                               "Введите число, о котором нужен факт, или любое слово"
                                               " для получения факта о случайном числе")
                self.bot.register_next_step_handler(answer, self.create_math_fact)
            elif callback_data == "date":
                answer = self.bot.send_message(call.message.chat.id,
                                               "Введите дату в формате месяц/день, о которой нужен факт,"
                                               "или любое слово для получения факта о случайной дате")
                self.bot.register_next_step_handler(answer, self.create_date_fact)
            elif callback_data == "year":
                answer = self.bot.send_message(call.message.chat.id,
                                               "Введите год, о котором нужен факт, или любое слово "
                                               "для получения факта о случайном годе")
                self.bot.register_next_step_handler(answer, self.create_year_fact)

    def create_trivia_fact(self, message):
        value = message.text
        if not value.isdigit():
            fact = translate(self.api.get_trivia_fact())
        else:
            fact = translate(self.api.get_trivia_fact(int(value)))
        self.bot.send_message(message.chat.id, fact)
        self.make_keyboard(message, Commands.KEYBOARD_TEXT.value)

    def create_math_fact(self, message):
        value = message.text
        if not value.isdigit():
            fact = translate(self.api.get_math_fact())
        else:
            fact = translate(self.api.get_math_fact(int(value)))
        self.bot.send_message(message.chat.id, fact)
        self.make_keyboard(message, Commands.KEYBOARD_TEXT.value)

    def create_date_fact(self, message):
        value = message.text
        pattern = r'^\d+/\d+$'
        if re.match(pattern, value) is None:
            fact = translate(self.api.get_date_fact())
        else:
            fact = translate(self.api.get_date_fact(value))
        self.bot.send_message(message.chat.id, fact)
        self.make_keyboard(message, Commands.KEYBOARD_TEXT.value)

    def create_year_fact(self, message):
        value = message.text
        if not value.isdigit():
            fact = translate(self.api.get_year_fact())
        else:
            fact = translate(self.api.get_year_fact(int(value)))
        self.bot.send_message(message.chat.id, fact)
        self.make_keyboard(message, Commands.KEYBOARD_TEXT.value)


class RunBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        ButtonsHandler(self.bot)
        self.bot.polling()
