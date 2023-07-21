import sqlite3

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

conn = sqlite3.Connection("store.db",check_same_thread=False)
cursor = conn.cursor()


async def start_key():
    mark = InlineKeyboardMarkup()
    mark.add(InlineKeyboardButton("Новая задача",callback_data="newTask"))
    mark.add(InlineKeyboardButton("Завершить задачу",callback_data="finishTask"))
    mark.add(InlineKeyboardButton("Список задач",callback_data="listTask"))
    mark.add(InlineKeyboardButton("Удалить задачу",callback_data="delTask"))
    return mark


async def showTasksToFinish():
    mark = InlineKeyboardMarkup()
    cursor.execute("SELECT * FROM user_data WHERE status = 1")
    dataTasks = cursor.fetchall()
    for task in dataTasks:
        mark.add(InlineKeyboardButton(task[2],callback_data=f"finish:{task[0]}"))
    mark.add(InlineKeyboardButton("Назад",callback_data="back_menu"))
    return mark


async def showAllTasks():
    mark = InlineKeyboardMarkup()
    cursor.execute("SELECT * FROM user_data")
    tasks = cursor.fetchall()
    for task in tasks:
        mark.add(InlineKeyboardButton(f"{task[2]}:{'Активная' if task[3]==1 else 'Завершено'}",callback_data="pass"))
    mark.add(InlineKeyboardButton("Назад", callback_data="back_menu"))
    return mark


async def deleteTask():
    mark = InlineKeyboardMarkup()
    cursor.execute("SELECT * FROM user_data")
    tasks = cursor.fetchall()
    for task in tasks:
        mark.add(InlineKeyboardButton(f"{task[2]}:{'Активная' if task[3] == 1 else 'Завершено'}", callback_data=f"delete:{task[0]}"))
    mark.add(InlineKeyboardButton("Назад", callback_data="back_menu"))
    return mark
