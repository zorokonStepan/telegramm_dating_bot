from aiogram.dispatcher.filters.state import StatesGroup, State


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
