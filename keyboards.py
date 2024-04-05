import asyncpg
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from config import user, password, db_name, host


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="➕Добавить книгу",
        callback_data="addbook")
    )
    builder.add(types.InlineKeyboardButton(
        text="🗑Удалить книгу",
        callback_data="delbook")
    )
    builder.add(types.InlineKeyboardButton(
        text="📕Список книг",
        callback_data="listbooks")
    )
    builder.add(types.InlineKeyboardButton(
        text="🔍Поиск книги",
        callback_data="searchbook")
    )
    builder.adjust(2)
    return builder.as_markup()


def button_save_book() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="✅Сохранить книгу",
        callback_data="savebook")
    )
    builder.adjust(1)
    return builder.as_markup()


def genre_selection_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Роман",
        callback_data="genre_selection:roman")
    )
    builder.add(types.InlineKeyboardButton(
        text="Рассказ",
        callback_data="genre_selection:fairy")
    )
    builder.add(types.InlineKeyboardButton(
        text="Повесть",
        callback_data="genre_selection:story")
    )
    builder.adjust(3)
    return builder.as_markup()


def keyboard_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Меню",
        callback_data="menu:1")
    )
    builder.adjust(3)
    return builder.as_markup()


async def all_books() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    for id, name_book, autor_book in await conn.fetch('''SELECT id, name, autor FROM book_libry'''):
        builder.add(
            types.InlineKeyboardButton(text=f"{name_book} | {autor_book}", callback_data=f"book:{id}")
        )
    builder.add(types.InlineKeyboardButton(
        text="📁Отсортировать по жанру",
        callback_data='genre_sort')
    )
    builder.add(types.InlineKeyboardButton(
        text="Меню",
        callback_data="menu:1")
    )
    builder.adjust(1)
    return builder.as_markup()


async def all_genre_roman() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    roman = "роман"
    for id, name_book, autor_book in await conn.fetch('''SELECT id, name, autor FROM book_libry WHERE genre = $1''', roman):
        builder.add(
            types.InlineKeyboardButton(text=f"{name_book} | {autor_book}", callback_data=f"book:{id}")
        )
    builder.add(types.InlineKeyboardButton(
        text="Меню",
        callback_data="menu:1")
    )
    builder.adjust(1)
    return builder.as_markup()


async def all_genre_fairy() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    fairy = "рассказ"
    for id, name_book, autor_book in await conn.fetch('''SELECT id, name, autor FROM book_libry WHERE genre = $1''', fairy):
        builder.add(
            types.InlineKeyboardButton(text=f"{name_book} | {autor_book}", callback_data=f"book:{id}")
        )
    builder.add(types.InlineKeyboardButton(
        text="Меню",
        callback_data="menu:1")
    )
    builder.adjust(1)
    return builder.as_markup()


async def all_genre_story() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    story = "повесть"
    for id, name_book, autor_book in await conn.fetch('''SELECT id, name, autor FROM book_libry WHERE genre = $1''', story):
        builder.add(
            types.InlineKeyboardButton(text=f"{name_book} | {autor_book}", callback_data=f"book:{id}")
        )
    builder.add(types.InlineKeyboardButton(
        text="Меню",
        callback_data="menu:1")
    )
    builder.adjust(1)
    return builder.as_markup()


async def all_books_del() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    conn = await asyncpg.connect(
        user=user,
        password=password,
        database=db_name,
        host=host
    )
    for id, name_book, autor_book in await conn.fetch('''SELECT id, name, autor FROM book_libry'''):
        builder.add(
            types.InlineKeyboardButton(text=f"{name_book} | {autor_book}", callback_data=f"del:{id}")
        )
    builder.add(types.InlineKeyboardButton(
        text="Назад",
        callback_data="menu:1")
    )
    builder.adjust(1)
    return builder.as_markup()
