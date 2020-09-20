import argparse
import codecs
import os.path
import sys
from collections import OrderedDict


def parse():
    """Создает парсер параметров из консоли"""
    parser = argparse.ArgumentParser(description='Text index project')
    parser.add_argument('input', type=str, help='Input file name')
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output.txt',
        help='Output file name (default: "output.txt")'
    )
    parser.add_argument(
        '-rs', '--remove_sps',
        action='store_true',
        help='Builds an output without service parts of speech'
    )
    parser.add_argument(
        '-com', '--print_common',
        type=int,
        default=0,
        help='Prints the specified number of the most common words (default: 0)'
    )
    return parser.parse_args()


class Word:
    def __init__(self, word, pages, quantity):
        self.word = word
        self.pages = pages
        self.quantity = quantity
    pages = []

    def __gt__(self, other):
        return self.quantity < other.quantity


def make_word_list(string):
    """Превращает строку в список русских слов и дефисов"""
    allowed_symbols = frozenset('абвгдеёжзийклмнопрстуфхцчшщъыьэюя-')
    string = string.lower()
    for char in string:
        if char not in allowed_symbols:
            string = string.replace(char, ' ')
    return string.split()


def hyphen_check(wrd):
    """Решает большую часть проблем, связанных с дефисами в словах"""
    if wrd.count('-') == 0:
        return wrd
    elif wrd.count('-') > 1:
        return ''
    else:
        if wrd.count('-с') == 1:
            return wrd[:-2]
        elif len(wrd) < 4:
            return ''
        else:
            return wrd


def update_dictionary(diction, wrd, page_num, banned_wrds):
    """Обновляет словарь данными об указанном слове, если оно не запрещено"""
    if wrd not in banned_wrds:
        if wrd in diction:
            if page_num not in diction[wrd].pages:
                diction[wrd].pages.append(page_num)
            diction[wrd].quantity += 1
        else:
            diction[wrd] = Word(wrd, [page_num], 1)
    return diction


def print_dictionary(diction, fvar):
    """Переписывает содержимое словаря в указанный файл"""
    for key in diction.keys():
        fvar.write(key + ': ')
        counter = 0
        for it in range(len(diction[key].pages) - 1):
            fvar.write(str(diction[key].pages[it]) + ', ')
            counter += 1
            if counter == 15:
                fvar.write('\n')
                counter = 0
        fvar.write(str(diction[key].pages[len(diction[key].pages) - 1]) + ';\n')


def make_banlist(par):
    """Генерирует список запрещенных слов на основе указанного файла"""
    banned_wrds = set()
    if par.remove_sps:
        with open('Service_parts_of_speech.txt', 'r', encoding='utf-8') as f_ban:
            banned_wrds = set(f_ban.read().splitlines())
    return banned_wrds


def print_most_common(diction, printsize):
    """Выводит в консоль указанное пользователем количество наиболее частотных слов"""
    if printsize > 0:
        diction = list(sorted(diction.values()))
        for i in range(min(printsize, len(diction))):
            print(f'{diction[i].word}: {diction[i].quantity};')


def main():
    PAGE_SIZE = 45
    set_io = parse()
    if not os.path.isfile(set_io.input):
        print(f'File "{set_io.input}" doesn\'t exist in this directory')
        sys.exit(2)
    banned_words = make_banlist(set_io)
    fin = open(set_io.input, 'r', encoding='utf-8')
    dictionary = {}
    page_number = 1
    line_number = 0
    for line in fin:
        if not line.isspace() and not line == '':
            line_number += 1
        page_number += line_number // PAGE_SIZE
        line_number %= PAGE_SIZE
        word_list = make_word_list(line)
        for new_word in word_list:
            if hyphen_check(new_word) != '':
                dictionary = update_dictionary(dictionary, hyphen_check(new_word), page_number, banned_words)
    fout = open(set_io.output, 'w', encoding='utf-8')
    dictionary = OrderedDict(sorted(dictionary.items()))
    fin.close()
    print_dictionary(dictionary, fout)
    fout.close()
    print_most_common(dictionary, set_io.print_common)


if __name__ == '__main__':
    main()
