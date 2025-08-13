import telebot
from telebot import types

TOKEN = 'your_token'

bot = telebot.TeleBot(TOKEN)

quiz_questions = [
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["7", "8", "9", "10"],
        "correct": "8"
    },
    {
        "question": "Какая самая длинная река в мире?",
        "options": ["Амазонка", "Нил", "Янцзы", "Миссисипи"],
        "correct": "Амазонка"
    },
    {
        "question": "Столица Австралии?",
        "options": ["Сидней", "Мельбурн", "Канберра", "Перт"],
        "correct": "Канберра"
    }
]

user_scores = {}
user_current_question = {}

def start_bot():
    print('Бот запущен')
    bot.polling(none_stop=True)

@bot.message_handler(commands=['start', 'restart'])
def start_quiz(message):
    chat_id = message.chat.id
    user_scores[chat_id] = 0
    user_current_question[chat_id] = 0
    bot.send_message(chat_id, 'Приветствуем вас в викторине! 🧠\nОтвечайте на вопросы, выбирая один из вариантов ответа.')
    send_question(chat_id)

def send_question(chat_id):
    if chat_id not in user_current_question:
        bot.send_message(chat_id, 'Нет доступа')
        return
    
    question_index = user_current_question[chat_id]
    
    if question_index >= len(quiz_questions):
        score = user_scores[chat_id]
        total = len(quiz_questions)
        bot.send_message(
            chat_id,
            f'🏆 Викторина завершена!\nВаш результат: {score} из {total}',
            reply_markup=types.ReplyKeyboardRemove()
        )
        del user_current_question[chat_id]
        del user_scores[chat_id]
        return
    
    question = quiz_questions[question_index]
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in question["options"]:
        markup.add(types.KeyboardButton(option))
    markup.add(types.KeyboardButton("❌ Завершить викторину"))
    
    bot.send_message(
        chat_id,
        f"Вопрос {question_index + 1}/{len(quiz_questions)}:\n{question['question']}",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.chat.id in user_current_question)
def check_answer(message):
    chat_id = message.chat.id
    question_index = user_current_question[chat_id]
    
    if message.text == "❌ Завершить викторину":
        score = user_scores[chat_id]
        total = len(quiz_questions)
        bot.send_message(
            chat_id,
            f"Викторина прервана.\nВаш результат: {score} из {total}",
            reply_markup=types.ReplyKeyboardRemove()
        )
        del user_current_question[chat_id]
        del user_scores[chat_id]
        return
    
    
    
    question = quiz_questions[question_index]
    
    if message.text == question['correct']:
        user_scores[chat_id] += 1
        bot.send_message(chat_id, "✅ Правильно!")
    else:
        correct_answer = question['correct']
        bot.send_message(chat_id, f"❌ Неправильно! Правильный ответ: {correct_answer}")
    
    user_current_question[chat_id] += 1
    send_question(chat_id)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(
        message.chat.id,
        "Я викторин-бот! Напишите /start чтобы начать викторину."
    )

if __name__ == "__main__":
    start_bot()
