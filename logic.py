from dataclasses import replace
import re
from PyPDF2 import PdfReader
from pydantic.v1.typing import update_field_forward_refs


# исчем слова в документе
def find_words(path, word):
    pages = [] # страницы, в которых содержатся искомые слова
    words = []
    word = word.lower()
    word_counter = 0 # подсчет слов

    # открываем текстовый документ, полученный на входе
    with open(path, 'rb') as file:
        pdf = PdfReader(file)

        pages_in_document = len(pdf.pages)

        for i in range(pages_in_document):
            text = pdf.pages[i].extract_text()

            if not text:
                continue

            # форматируем текс, убираем все символы кроме букв
            text = re.sub(r'[^a-zA-Zа-яA-ЯёЁ\s]', '', text.lower())
            text = text.split()

            # считаем искомые слова на странице
            count = text.count(word)


            if count > 0:
                pages.append(i)

                word_counter += count

    return pages, word_counter


# выводим искомый текст
def show_text(path, page):
    with open(path, 'rb') as file:
        pdf = PdfReader(file)

        text = pdf.pages[page]

        return text.extract_text()


# считаем все слова в документе
def count_words(path):
    words = 0
    with open(path, 'rb') as file:
        pdf = PdfReader(file)

        pages = pdf.pages

        for page in range(len(pages)):
            page_ = pdf.pages[page]
            text = page_.extract_text().lower()

            text = text.split(' ')

        return len(text)

# расчитываем tf
def get_tf(path, searched_word):
    words = count_words(path)

    return searched_word / words








