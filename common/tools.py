from django.template.defaultfilters import slugify
import random
import string

_capital_letters = {
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'E',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'H',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Sch',
    'Ъ': '',
    'Ы': 'Y',
    'Ь': '',
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya',
}

_lower_case_letters = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}

def transliterate(_string):
    try:
        string = str(_string)
    except Exception as e:
        # raise e
        string = _string  

    capital_letters = _capital_letters
    lower_case_letters = _lower_case_letters

    len_str = len(string)

    translit_string = ""

    for index, char in enumerate(string, 1):
        repl = lower_case_letters.get(char)
        if repl:
            translit_string += repl
            continue

        repl = capital_letters.get(char)
        if repl:
            if len_str > index:
                if string[index] not in lower_case_letters:
                    repl = repl.upper()
            else:
                repl = repl.upper()
        else:
            repl = char

        translit_string += repl

    return translit_string

def make_url(_string=''):
    if not _string:
        chars = string.ascii_uppercase + string.digits
        _string = ''.join(random.choice(chars) for _ in range(6))

    return slugify(transliterate(_string.lower()))
