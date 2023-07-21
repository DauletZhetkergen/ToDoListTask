import asyncio
import configparser

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

import keyboard

config = configparser.ConfigParser()

config.read("settings.ini")

TOKEN = config["BASIC"]["TOKEN"]

conn = sqlite3.Connection("store.db",check_same_thread=False)
cursor = conn.cursor()

bot = Bot(TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())


class Adder(StatesGroup):
    name = State()


@dp.message_handler(commands=["start", "menu"], state='*')
async def start(message: types.Message):
    await message.answer("Приветствую",reply_markup= await keyboard.start_key())

@dp.callback_query_handler(lambda message: message.data == "back_menu")
async def newTask(call: types.CallbackQuery):
    await call.message.edit_text("Приветствую",reply_markup= await keyboard.start_key())





@dp.callback_query_handler(lambda message: message.data == "newTask")
async def newTask(call: types.CallbackQuery):
    await call.message.edit_text("Напишите задание")
    await Adder.name.set()



@dp.message_handler(state=Adder.name)
async def nameProduct(message: types.Message, state: FSMContext):
    if message.text.isdigit():  #Проверяет сообщения от юзера, если только цифры задача не запишется
                                #Отправить сообщение снизу и запросит новую задачу
        await message.answer("Напишите задачу а не цифры")
        await Adder.name.set()
    else:
        cursor.execute("INSERT INTO user_data(user_id,task_text,status) VALUES (?,?,?)",
                                                                                (message.from_user.id,message.text,1))
        conn.commit()
        await state.finish()
        await message.answer("Задача добавлена")
        await asyncio.sleep(0.3)
        await message.answer("Меню",reply_markup= await keyboard.start_key())

@dp.callback_query_handler(lambda message: message.data == "finishTask")
async def finishTask(call: types.CallbackQuery):
    await call.message.edit_text("Выберите задачу",reply_markup=await keyboard.showTasksToFinish())



@dp.callback_query_handler(text_contains="finish")
async def finishTask2(call: types.CallbackQuery, state: FSMContext):
    taskID = call.data.split(":")[1]
    cursor.execute("UPDATE user_data SET status = 0 WHERE id = ?",(taskID,))
    conn.commit()
    await call.message.edit_text("Задача завершена")
    await asyncio.sleep(1)
    await call.message.edit_text("Меню", reply_markup=await keyboard.start_key())

@dp.callback_query_handler(lambda message: message.data == "listTask")
async def listTask(call: types.CallbackQuery):
    await call.message.edit_text("Список задач",reply_markup=await keyboard.showAllTasks())




@dp.callback_query_handler(lambda message: message.data == "delTask")
async def deleteTask(call: types.CallbackQuery):
    await call.message.edit_text("Выберите задачу для удаления",reply_markup= await keyboard.deleteTask())

@dp.callback_query_handler(text_contains="delete")
async def deleteTaskConfirm(call: types.CallbackQuery, state: FSMContext):
    taskID = call.data.split(":")[1]
    cursor.execute("DELETE FROM user_data WHERE id = ?",(taskID,))
    conn.commit()
    await call.message.edit_text("Удалено")
    await asyncio.sleep(1)
    await call.message.edit_text("Меню", reply_markup=await keyboard.start_key())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






