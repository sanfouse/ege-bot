from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from aiogram.types.web_app_info import WebAppInfo

from .buttons import *


def start_menu_keyboard():

  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

  markup.add(ABOUT_USER)

  return markup



def check_question_keyboard(number):
    markup = InlineKeyboardMarkup(row_width=2)
  
    markup.add(
                InlineKeyboardButton(
                    MENU,
                    callback_data=f'menu {number}'
                )
    )

    return markup


def check_questions_keyboard_true(number, url):

  markup = InlineKeyboardMarkup(row_width=2)
  
  markup.add(
                InlineKeyboardButton(
                    MENU,
                    callback_data=f'menu {number}'
                ),
                InlineKeyboardButton(
                    ABOUT,
                    web_app=WebAppInfo(url=url)
                )
            )

  markup.add(
                InlineKeyboardButton(
                            NEXT,
                            callback_data=number
                        )
            )


  return markup


def check_questions_keyboard_false(number, url):

  markup = InlineKeyboardMarkup(row_width=2)
  
  markup.add(
                InlineKeyboardButton(
                    MENU,
                    callback_data=f'menu {number}'
                ),
                InlineKeyboardButton(
                    ABOUT,
                    web_app=WebAppInfo(url=url)
                )
            )

  return markup


def numbers_menu_keyboard():

    markup = InlineKeyboardMarkup(row_width=3)

    for number in range(1, 25, 3):

        markup.add(
                InlineKeyboardButton(
                            f'Номер {number}',
                            callback_data=f'{number}'
                        ),
                InlineKeyboardButton(
                            f'Номер {number + 1}',
                            callback_data=f'{number + 1}'
                        ),
                InlineKeyboardButton(
                            f'Номер {number + 2}',
                            callback_data=f'{number + 2}'
                        )
            )
    
    return markup


