from aiogram.dispatcher.filters.state import StatesGroup, State

'''
class Reg - состояния во время регистрации нового пользователя
class Change - состояния во время изменения настроек пользователя
class AdminChangeClient - состояния во время изменения настроек администратором у пользователя
'''


class Reg(StatesGroup):
    Name = State()
    Age = State()
    Gender = State()
    Biography = State()
    Photo = State()
    Location = State()
    SearchGender = State()
    SearchAge = State()
    SearchLocation = State()
    SearchRadius = State()


class Change(StatesGroup):
    Name = State()
    Age = State()
    Gender = State()
    Biography = State()
    Photo = State()
    Location = State()
    SearchGender = State()
    SearchAge = State()
    SearchLocation = State()
    SearchRadius = State()


class AdminChangeClient(StatesGroup):
    Name = State()
    Age = State()
    Gender = State()
    Biography = State()
    Photo = State()
    Location = State()
    SearchGender = State()
    SearchAge = State()
    SearchLocation = State()
    SearchRadius = State()
