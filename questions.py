import asyncpg
from aiogram import Router, F, types
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboard.keyboards import main_menu, button_save_book, all_books, genre_selection_keyboard, all_genre_roman, all_genre_fairy, all_genre_story, all_books_del, keyboard_menu
from data.config import user, password, db_name, host

router = Router()

# Обработчик основной команды start
@router.message(CommandStart())
async def command_start(message: types.Message):
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )

    # Создание базы данных
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS book_library(
            id SERIAL PRIMARY KEY,
            name TEXT,
            autor TEXT,
            info TEXT,
            genre TEXT
        )''')
    reply_menu = main_menu()
    await message.answer(text="Привет дорогие модераторы или модератор не знаю сколько вас там проверяет, желаю вам хорошего дня! и давайте начнем.", reply_markup=reply_menu)


class BookInfo(StatesGroup):
    name = State()
    autor = State()
    info = State()
    genre = State()

# Обработчик для кнопки "Добавить книгу"
@router.callback_query(F.data == 'addbook')
async def add_book(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝Введите название книги")
    await state.set_state(BookInfo.name)

# Обработчики стейтов
@router.message(BookInfo.name)
async def state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer("📝Введите автора книги")
    await state.set_state(BookInfo.autor)

@router.message(BookInfo.autor)
async def state_autor(message: types.Message, state: FSMContext):
    await state.update_data(autor=message.text.lower())
    await message.answer("📝Напишите описание книги")
    await state.set_state(BookInfo.info)

@router.message(BookInfo.info)
async def state_info(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text.lower())
    await message.answer("📝Введите свой жанр книги или выберите ниже")
    await state.set_state(BookInfo.genre)

@router.message(BookInfo.genre)
async def state_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text.lower())
    reply_keyboard = button_save_book()
    await message.answer("Нажмите на кнопку", reply_markup=reply_keyboard)
    global data
    data = await state.get_data()
    await state.clear()

# Обработчик кнопки для добавления книги в БД
@router.callback_query(F.data == "savebook")
async def save_book(callback: types.CallbackQuery):
    reply_keyboard = main_menu()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    await conn.execute(
        '''INSERT INTO book_library(name, autor, info, genre) 
        VALUES($1, $2, $3, $4)''',
        data['name'], data['autor'], data['info'], data['genre']
    )
    await conn.close()
    await callback.message.edit_text("Меню:", reply_markup=reply_keyboard)

# Обработка кнопки для вывода инструкции
@router.callback_query(F.data == "searchbook")
async def search_button(callback: types.CallbackQuery):
    reply_keyboard = keyboard_menu()
    await callback.message.edit_text("Введите Ключевое слово которое есть в названии или имени автора что бы найти книгу, так же можете вводить хоть одну букву и бот покажет вам все книги которые имеют эту букву в названии и тд. \n Команда: /search", reply_markup=reply_keyboard)

#выводит все книги из бд
@router.callback_query(F.data == "listbooks")
async def list_button(callback: types.CallbackQuery):
    reply_keyboard = await all_books()
    await callback.message.edit_text("Список - ", reply_markup=reply_keyboard)

#обработчик вывода информации о книге
@router.callback_query(F.data.startswith("book:"))
async def info_book(callback: types.CallbackQuery):
    reply_keyboard = keyboard_menu()
    book_id = int(callback.data.split(":")[1])
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    for id, name, autor, genre in await conn.fetch('''SELECT id, name, autor, genre FROM book_libry WHERE id = $1''', book_id):
        await callback.message.edit_text(f"Номер книги - {id}\n Название - {name}\n Автор - {autor}\n Жанр - {genre}", reply_markup=reply_keyboard)

#обработчик кнопки фильтров сортировки
@router.callback_query(F.data == "genre_sort")
async def genre_filtr_button(callback: types.CallbackQuery):
    reply_keyboard = await genre_selection_keyboard()
    await callback.message.edit_text("Выберите по какому жанру вы хотите отсортировать:", reply_markup=reply_keyboard)

#обработка кнопок сортировки по жанрам
@router.callback_query(F.data.startswith("genre:"))
async def genre_list_button(callback: types.CallbackQuery):
    action = callback.data.split(":")[1]
    if action == "roman":
        reply_keyboard = await all_genre_roman()
        await callback.message.edit_text("Книги по выбранному жанру -", reply_markup=reply_keyboard)
    if action == "fairy":
        reply_keyboard = await all_genre_fairy()
        await callback.message.edit_text("Книги по выбранному жанру -", reply_markup=reply_keyboard)
    if action == "story":
        reply_keyboard = await all_genre_story()
        await callback.message.edit_text("Книги по выбранному жанру -", reply_markup=reply_keyboard)

#Поиск книг в бд по ключевому слову
async def search_books(keyword):
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    books = await conn.fetch('''SELECT id, name, autor FROM book_libry WHERE name ILIKE $1 OR autor ILIKE $1''', f'%{keyword}%')
    await conn.close()
    return books

#Обработчик команды для поиска книги
@router.message(Command('search'))
async def search_books_command(message: types.Message, command: CommandObject):
    keyword = command.args
    found_books = await search_books(keyword)
    
    if found_books:
        builder = InlineKeyboardBuilder()
        for book in found_books:
            builder.add(types.InlineKeyboardButton(text=f"{book['name']} - {book['autor']}", callback_data=f"book:{book['id']}"))
        
        await message.answer("Найденные книги:", reply_markup=builder.as_markup())
    else:
        await message.answer("Книги не найдены")

#обработка всех кнопок которые играют роль в перемещении в меню
@router.callback_query(F.data.startswith("menu:"))
async def handlers_menu(callback: types.CallbackQuery):
    data = callback.data.split(":")[1]
    if data == "1":
        reply_keyboard = main_menu()
        await callback.message.edit_text("Меню", reply_markup=reply_keyboard)

#обработка списка книг которые можно выбрать и удалить
@router.callback_query(F.data == "delbook")
async def book_del_button(callback: types.CallbackQuery):
    reply_keyboard = await all_books_del()
    await callback.message.edit_text("выберите книгу для удаления:", reply_markup=reply_keyboard)

#обработка удаления книги
@router.callback_query(F.data.startswith("del:"))
async def books_del(callback: types.CallbackQuery):
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    data = int(callback.data.split(":")[1])
    reply_keyboard = keyboard_menu()
    await conn.execute("DELETE FROM book_libry WHERE id = $1", data)
    await callback.message.edit_text("Книга удалена!", reply_markup=reply_keyboard)
