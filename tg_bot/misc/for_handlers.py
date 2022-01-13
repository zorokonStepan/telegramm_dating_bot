from asyncio import sleep

from create_bot import bot
from config import time_sleep


async def sleep_del_msg_message(msg, message):
    await sleep(time_sleep)
    await msg.delete()
    await message.delete()


async def state_finish_sleep_bot_del_msg_message_delete(message, state, msg):
    await state.finish()
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await message.delete()


async def sleep_bot_delete_msg_message_delete(msg, message):
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await message.delete()


async def state_save_data_sleep_bot_delete_msg(state, callback_data, msg):
    async with state.proxy() as data:
        data["callback_data"] = callback_data
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


async def sleep_bot_del_msg(msg):
    await sleep(time_sleep)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
