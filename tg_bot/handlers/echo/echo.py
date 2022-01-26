from aiogram import types, Dispatcher

from tg_bot.handlers.templetes_handlers.tmp_misc import sleep_bot_delete_msg_message_delete


async def echo_send(message: types.Message):
    msg = await message.answer(f"Неизвестная команда: {message.text}")
    await sleep_bot_delete_msg_message_delete(msg, message)


def register_echo_hs(dp: Dispatcher):
    dp.register_message_handler(echo_send)
