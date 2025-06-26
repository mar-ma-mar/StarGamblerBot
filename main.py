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

# Клавиатура для стартового меню с двумя кнопками
start_keyboard = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(
        text="🧠 Сделать ставку",
        web_app=WebAppInfo(url="https://funny-biscuit-ccf218.netlify.app") 
    ),
    InlineKeyboardButton(
        text="📅 Показать события",
        callback_data="show_events"
    )
)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в *Ставь на Будущее*!\n\n"
        "Выбери действие ниже:",
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "show_events")
async def show_events(callback_query: types.CallbackQuery):
    for event in events:
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            InlineKeyboardButton("✅ Да", callback_data=f"vote:{event['id']}:yes"),
            InlineKeyboardButton("❌ Нет", callback_data=f"vote:{event['id']}:no"),
            InlineKeyboardButton("ℹ️ Подробнее", callback_data=f"more:{event['id']}")
        )
        await bot.send_message(
            callback_query.from_user.id,
            f"*{event['title']}*\n{event['desc']}",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("vote:"))
async def handle_vote(callback_query: types.CallbackQuery):
    _, event_id, choice = callback_query.data.split(":")
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы проголосовали:\nСобытие: `{event_id}`\nВаш выбор: {'Да' if choice == 'yes' else 'Нет'}",
        parse_mode="Markdown"
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("more:"))
async def more_info(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split(":")[1]
    event = next((e for e in events if e["id"] == event_id), None)
    if event:
        await bot.send_message(
            callback_query.from_user.id,
            f"📄 *Подробности о событии {event_id}*\n\n{event['desc']}\n\n_Пока информации немного, но скоро будет больше!_",
            parse_mode="Markdown"
        )
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
