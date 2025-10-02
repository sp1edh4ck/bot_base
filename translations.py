"""
You can add multiple languages for translation.

An example of using a function in the code:

await bot.send_message(
    message.from_user.id,
    _('Your text.', 'lang_code')
)
"""


translation = {
    'en': {
        'Ваш текст': 'Your text',
    }
}


def _(text, lang='ru'):
    if lang == 'ru':
        return text
    else:
        global translation
        try:
            return translation[lang][text]
        except:
            return text
