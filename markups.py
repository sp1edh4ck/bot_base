"""
Below is an example of two buttons:

1. Basic inline button.
2. A set of buttons according to the list, for example,
    if you do not know how many buttons there will be.
"""


from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from translations import _


def btn_start():
    btn_start = InlineKeyboardButton(text="start", callback_data='btn_start')
    kb = InlineKeyboardBuilder().row(btn_start, width=1)
    return kb


def btn_list(lang, list):
    kb = InlineKeyboardBuilder()
    for index, list_object in enumerate(list):
        btn_object = InlineKeyboardButton(text=_(f"Object {list_object[0]}"), callback_data=f"btn_object_{list_object[0]}")
        if (index + 1) % 2 == 0: # You can put the required number of buttons in one row instead of 2.
            kb.add(btn_object)
        else:
            kb.row(btn_object)
    btn_additional = InlineKeyboardButton(text=_("👈 Назад", lang), callback_data="btn_additional")
    kb.row(btn_additional)
    return kb
