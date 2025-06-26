from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

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

# Для простоты — словарь голосов пользователя, чтобы показывать, что уже проголосовал
user_votes = {}

def build_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("📋 Список событий", callback_data="show_events"))
    keyboard.add(InlineKeyboardButton("ℹ️ Помощь", callback_data="help"))
    return keyboard

def build_event_keyboard(event_id, user_id):
    # Если пользователь уже голосовал за это событие
    voted = user_votes.get(user_id, {}).get(event_id)
    if voted:
        text = "✅ Вы проголосовали: " + ("Да" if voted == "yes" else "Нет")
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text, callback_data="noop"))
        keyboard.add(InlineKeyboardButton("ℹ️ Подробнее", callback_data=f"more:{event_id}"))
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Да", callback_data=f"vote:{event_id}:yes"),
            InlineKeyboardButton("❌ Нет", callback_data=f"vote:{event_id}:no"),
        )
        keyboard.add(InlineKeyboardButton("ℹ️ Подробнее", callback_data=f"more:{event_id}"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в *Ставь на Будущее*!\n\n"
        "Здесь вы можете ставить на события будущего и делиться своим мнением.\n"
        "Нажмите кнопку ниже, чтобы увидеть список доступных событий.",
        parse_mode="Markdown",
        reply_markup=build_main_menu()
    )

@dp.callback_query_handler(lambda c: c.data == "show_events")
async def show_events(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    for idx, event in enumerate(events, start=1):
        text = f"*Событие {idx} из {len(events)}*\n\n*{event['title']}*\n{event['desc']}"
        keyboard = build_event_keyboard(event["id"], user_id)
        await bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("vote:"))
async def handle_vote(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    _, event_id, choice = callback_query.data.split(":")
    
    # Сохраняем голос
    user_votes.setdefault(user_id, {})[event_id] = choice
    
    answer = "✅ Ты выбрал 'Да'" if choice == "yes" else "❌ Ты выбрал 'Нет'"
    await bot.send_message(user_id, f"Спасибо за ставку на событие *{event_id}*!\n{answer}", parse_mode="Markdown")
    
    # Отправляем обновлённое сообщение с пометкой о голосе
    event = next((e for e in events if e["id"] == event_id), None)
    if event:
        keyboard = build_event_keyboard(event_id, user_id)
        text = f"*{event['title']}*\n\n{event['desc']}"
        await bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=keyboard)
    
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith("more:"))
async def more_info(callback_query: types.CallbackQuery):
    event_id = callback_query.data.split(":")[1]
    event = next((e for e in events if e["id"] == event_id), None)
    if event:
        await bot.send_message(callback_query.from_user.id, f"📄 *Подробности:*\n\n{event['desc']}\n\n_Пока подробностей немного, скоро добавим больше!_", parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == "help")
async def help_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "ℹ️ *Помощь*\n\n"
                           "/s
