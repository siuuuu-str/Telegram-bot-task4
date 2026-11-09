import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = "9259216256:AAGAWNQexWsQ38CxjaPVx1bi9Hh8mf28I7c"
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# Создаем состояния (шаги опроса)
class Survey(StatesGroup):
    name = State()
    age = State()
    hobby = State()

# Начало опроса
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # сбрасываем прошлые ответы
    await message.answer("Давай познакомимся! Как тебя зовут? (или напиши /cancel)")
    await state.set_state(Survey.name)

# Получаем имя
@dp.message(Survey.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Survey.age)

# Получаем возраст
@dp.message(Survey.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, напиши возраст цифрами.")
        return
    await state.update_data(age=message.text)
    await message.answer("Твое хобби?")
    await state.set_state(Survey.hobby)

# Получаем хобби и выводим сводку
@dp.message(Survey.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    
    # Достаем все данные
    user_data = await state.get_data()
    
    text = (f"Спасибо за ответы!\n\n"
            f"👤 Имя: {user_data['name']}\n"
            f"🎂 Возраст: {user_data['age']}\n"
            f"🎨 Хобби: {user_data['hobby']}")
    
    await message.answer(text)
    await state.clear() # Очищаем состояние после завершения

# Отмена опроса
@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять.")
        return
    await state.clear()
    await message.answer("Опрос отменен.")

async def main():
    print("Бот-опросник запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())