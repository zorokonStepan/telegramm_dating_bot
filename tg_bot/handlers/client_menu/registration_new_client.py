from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.schemas.users_commands import common_commands_users_db as commands
from tg_bot.database.schemas.users_commands.client_commands_users_db import add_client, update_state_client
from tg_bot.filters import IsNewClient
from tg_bot.handlers.all_users.start_main_menu import start_new_client
from tg_bot.keyboards.all_users.inline.all_users import get_gender_kb, get_search_gender_kb
from tg_bot.keyboards.callback_datas.cb_datas import gender_callback
from tg_bot.keyboards.client.reply.reply_registration_new_client import forth_kb, start_over_kb
from tg_bot.states import Reg


# 1. Принимаем и обрабатываем первый ответ пользователя - его имя. Переводим его на вопрос: возраст.
async def load_name(message: types.Message):
    await add_client(user_id=message.from_user.id, username=message.from_user.username, client_state="new_client",
                     name=message.text)
    await Reg.Age.set()
    await message.answer("Теперь укажите сколько вам полных лет: ")


# 2. Принимаем и обрабатываем ответ на возраст. Переводим на вопрос: пол
async def load_age(message: types.Message):
    if not (message.text).isdigit():
        await message.answer("Укажите сколько вам полных лет, используя только цифры: ")
    else:
        await commands.update_user_age(user_id=message.from_user.id, age=int(message.text))
        await Reg.Gender.set()
        await message.answer("Укажите кто вы, мужчина или женщина.",
                             reply_markup=get_gender_kb(params=["base", "reg_gender_kb"]))


# 3. Принимаем и обрабатываем ответ на пол. Переводим на вопрос: биография
async def load_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data_text = call.data.split(":")[1]
    # переписать как в файле с изменением настроек
    if data_text == "Мужчина" or data_text == 'Женщина':
        await commands.update_user_gender(call.from_user.id, data_text)
        await call.message.delete()
        await Reg.Biography.set()
        await call.message.answer("Расскажите о себе: ")


# 4. Принимаем и обрабатываем ответ на биографию. Переводим на вопрос: фото.
async def load_biography(message: types.Message, state: FSMContext):
    try:
        await commands.update_user_biography(message.from_user.id, message.text)
        await Reg.Photo.set()
        await message.answer("Загрузите фото с собой, от 1 до 10 штук.")
        await message.answer("Если вы закончили загружать фото, то нажмите кнопку 'Далее'.",
                             reply_markup=forth_kb)
    except Exception:
        await message.answer("Расскажите о себе чуть покороче: ")


# 5. Принимаем и обрабатываем ответ на фото. Переводим на вопрос: местоположение пользователя.
async def load_photo(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    if len(user.photo) == 0 and message.text == "Далее":
        await message.answer('Загрузите минимум одно фото')
    elif len(user.photo) < 10 and message.text != "Далее":
        await commands.append_user_photo(message.from_user.id, message.photo[0].file_id)
        user = await commands.select_user(message.from_user.id)
        await message.answer(f'{len(user.photo)} фото добавлено в ваш профиль.')
        if len(user.photo) == 10:
            await message.answer(f'{len(user.photo)} фото добавлено в ваш профиль.', reply_markup=ReplyKeyboardRemove())
            await Reg.Location.set()
            await message.answer("Отправьте свою локацию.", reply_markup=start_over_kb)

    else:
        await message.answer(f'{len(user.photo)} фото добавлено в ваш профиль.', reply_markup=ReplyKeyboardRemove())
        await Reg.Location.set()
        await message.answer("Отправьте свою локацию.", reply_markup=start_over_kb)


# 6. Принимаем и обрабатываем ответ на место нахождения пользователя. Переводим на поиск-пол.
async def load_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_latitude(message.from_user.id, latitude)
    await commands.update_user_longitude(message.from_user.id, longitude)
    await Reg.SearchGender.set()
    await message.answer("Кого вы ищите, мужчину или женщину?",
                         reply_markup=get_search_gender_kb(params=["base", "reg_search_gender_kb"]))


# 7. Принимаем и обрабатываем ответ на search gender. Переводим на поиск - возраст.
async def search_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data_text = call.data.split(":")[1]
    await commands.update_user_search_gender(call.from_user.id, data_text)
    await call.message.delete()
    await Reg.SearchAge.set()
    await call.message.answer("Укажите возраст кого вы ищите одним числом или диапозон двумя числами через пробел: ")


# 8. Принимаем и обрабатываем ответ на поиск - возраст. Переводим на поиск - локация.
async def search_age(message: types.Message):
    lst_age = (message.text).split()
    if "".join(lst_age).isdigit() and len(lst_age) == 2:
        lst_age = [int(lst_age[0]), int(lst_age[1])]
        lst_age = sorted(lst_age)
        await commands.update_user_search_age(message.from_user.id, lst_age)
        await Reg.SearchLocation.set()
        await message.answer("Отправьте локацию где будем искать: ", reply_markup=start_over_kb)
    else:
        await message.answer("Укажите возраст кого вы ищите одним числом или диапозон двумя числами через пробел: ")


# 9. Принимаем и обрабатываем ответ на место поиска. Переводим на радиус поиска.
async def search_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await commands.update_user_search_latitude(message.from_user.id, latitude)
    await commands.update_user_search_longitude(message.from_user.id, longitude)
    await Reg.SearchRadius.set()
    await message.answer("Укажите целое число, радиус поиска в километрах: ")


# 10. Принимаем и обрабатываем ответ на радиус поиска. Переводим пользователя в состояние ожидания проверки анкеты
# модератором.
async def search_radius(message: types.Message, state: FSMContext):
    if (message.text).isdigit():
        await commands.update_user_search_radius(message.from_user.id, int(message.text))
        await update_state_client(message.from_user.id, client_state="wait_client")
        await state.finish()
        await message.answer("Замечательно! Анкета заполнена. Модератор проверит ее и вы сможете пользоваться ботом. "
                             "О завершении проверки вам придет сообщение.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Укажите целое число, радиус поиска в километрах: ")


# 100
async def start_over(call: types.CallbackQuery, state: FSMContext):
    await commands.delete_user(call.from_user.id)
    await call.message.delete()
    await state.finish()
    await start_new_client(call.message)


# 100
async def start_over_2(message: types.Message, state: FSMContext):
    await commands.delete_user(message.from_user.id)
    await message.delete()
    await state.finish()
    await start_new_client(message)


def register_handlers_registration_new_client(dp: Dispatcher):
    dp.register_message_handler(load_name, state=Reg.Name)
    dp.register_message_handler(load_age, IsNewClient(), state=Reg.Age)
    dp.register_callback_query_handler(load_gender, IsNewClient(), gender_callback.filter(), state=Reg.Gender)
    dp.register_message_handler(load_biography, IsNewClient(), state=Reg.Biography)
    dp.register_message_handler(load_photo, IsNewClient(), text=['Далее'], state=Reg.Photo)
    dp.register_message_handler(load_photo, IsNewClient(), content_types=['photo'], state=Reg.Photo)
    dp.register_message_handler(load_location, IsNewClient(), content_types=types.ContentTypes.LOCATION,
                                state=Reg.Location)
    dp.register_callback_query_handler(search_gender, IsNewClient(), gender_callback.filter(), state=Reg.SearchGender)
    dp.register_message_handler(search_age, IsNewClient(), state=Reg.SearchAge)
    dp.register_message_handler(search_location, IsNewClient(), content_types=types.ContentTypes.LOCATION,
                                state=Reg.SearchLocation)
    dp.register_message_handler(search_radius, IsNewClient(), state=Reg.SearchRadius)

    dp.register_callback_query_handler(start_over, IsNewClient(), text="start_over", state="*")
    dp.register_message_handler(start_over_2, IsNewClient(), text="Начать с начала", state="*")
