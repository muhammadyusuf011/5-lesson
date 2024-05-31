from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton(text="User"))
    return rkm


def next_menu():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton(text="Add user"), KeyboardButton(text="View users"))
    rkm.row(KeyboardButton(text="Get user"), KeyboardButton(text="Update user"))
    return rkm

def update_menu():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    rkm.row(KeyboardButton(text="name"), KeyboardButton(text="age"))
    rkm.row(KeyboardButton(text="address"), KeyboardButton(text="photo"))
    return rkm