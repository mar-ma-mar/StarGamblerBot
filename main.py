import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Кнопка для открытия WebApp
webapp_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text="🧠 Сделать ставку",
        web_app=WebAppInfo(url="https://funny-biscuit-ccf218.netlify.app")
    )
)

# Список событий
events = [
    {
        "id": "mars2028",
        "title": "🚀 Маск полетит на Марс до 2028 года",
        "desc": "Сделает ли Иллон Маск пилотируемую миссию на Марс до конца 2027 года?",
    },
    {
        "id": "war2026",
        "title": "💥 Америка вступит в войну с Ираном в 2026 году",
        "desc": "Произойдёт ли военный конфликт между США и Ираном в ближайшие два года?",
    },
    {
        "id": "ai2027",
        "title": "🤖 ИИ захватит мир в 2027 году",
        "desc": "Станет ли ИИ доминирующей силой, заменяющей правительства и бизнес?",
    },
]

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в *Ставь на Будущее*!\n\nЖми на кнопку ниже:",
        parse_mode="Markdown",
        reply_markup=webapp_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "show_events")
async def show_events(callback_query: types.CallbackQuery):
    for event in events:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Да", callback_data=f"vote:{event['id']}:yes"),
            InlineKeyboardButton("❌ Нет", callback_data=f"vote:{event['id']}:no"),
            InlineKeyboardButton("ℹ️ Подробнее", callback_data=f"more:{event['id']}")
        )
        await bot.send_message(callback_query.from_user.id,
                               f"*{event['title']}*\n\n{event['desc']}",
                               parse_mode="Markdown",
                               reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("vote:"))
async def handle_vote(callback_query: types.CallbackQuery):
    _, event_id, choice = callback_query.data.split(":")
    answer = "✅ Ты выбрал 'Да'" if choice == "yes" else "❌ Ты выбрал 'Нет'"
    await bot.send_message(callback_query.from_user.id, f"Спасибо за ставку на событие `{event_id}`!\n{answer}",
                           parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("more:"))
async def more_info(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split(":")[1]
    event = next((e for e in events if e["id"] == event_id), None)
    if event:
        await bot.send_message(callback_query.from_user.id, f"📄 *Подробности:*\n\n{event['desc']}",
                               parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
