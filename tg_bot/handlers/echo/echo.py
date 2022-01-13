from aiogram import types, Dispatcher
import asyncio

from create_bot import bot


async def echo_send(message: types.Message):
    msg = await message.answer(f"Неизвестная команда: {message.text}")
    await asyncio.sleep(5)
    await message.delete()
    await bot.delete_message(msg.chat.id, msg.message_id)


def register_echo_hs(dp: Dispatcher):
    dp.register_message_handler(echo_send)
