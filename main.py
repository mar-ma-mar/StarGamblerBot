import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_balances = {}

@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 1000
        await message.answer("👋 Добро пожаловать! Твой стартовый баланс — 1000 звёзд.")
    else:
        await message.answer("Ты уже зарегистрирован!")

@dp.message(Command(commands=["balance"]))
async def cmd_balance(message: Message):
    user_id = message.from_user.id
    balance = user_balances.get(user_id, 0)
    await message.answer(f"Твой текущий баланс: {balance} звёзд.")

@dp.message(Command(commands=["bet"]))
async def cmd_bet(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /bet <сумма>")
        return
    amount = int(args[1])
    balance = user_balances.get(user_id, 0)
    if amount <= 0:
        await message.answer("Сумма ставки должна быть положительной.")
        return
    if balance < amount:
        await message.answer("Недостаточно звёзд для ставки.")
        return
    user_balances[user_id] -= amount
    await message.answer(f"Ставка {amount} звёзд принята! Остаток: {user_balances[user_id]} звёзд.")

@dp.message(Command(commands=["win"]))
async def cmd_win(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /win <сумма>")
        return
    amount = int(args[1])
    if amount <= 0:
        await message.answer("Сумма выигрыша должна быть положительной.")
        return
    user_balances[user_id] = user_balances.get(user_id, 0) + amount
    await message.answer(f"Поздравляем! Твой выигрыш: {amount} звёзд.\nБаланс: {user_balances[user_id]} звёзд.")

@dp.message(Command(commands=["transfer"]))
async def cmd_transfer(message: Message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) != 3 or not args[2].isdigit() or not args[1].startswith("@"):
        await message.answer("Использование: /transfer <@username> <сумма>")
        return
    receiver_username = args[1][1:]
    amount = int(args[2])
    sender_balance = user_balances.get(user_id, 0)
    if amount <= 0:
        await message.answer("Сумма перевода должна быть положительной.")
        return
    if sender_balance < amount:
        await message.answer("Недостаточно звёзд для перевода.")
        return

    try:
        receiver = await bot.get_chat(receiver_username)
    except Exception:
        await message.answer("Пользователь не найден.")
        return
    receiver_id = receiver.id

    user_balances[user_id] -= amount
    user_balances[receiver_id] = user_balances.get(receiver_id, 0) + amount

    await message.answer(f"Ты перевёл {amount} звёзд @{receiver_username}.\nБаланс: {user_balances[user_id]} звёзд.")
    await bot.send_message(receiver_id, f"Тебе перевели {amount} звёзд от @{message.from_user.username}!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
