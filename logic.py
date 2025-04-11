from dataclasses import replace
import re
from PyPDF2 import PdfReader
from pydantic.v1.typing import update_field_forward_refs


def find_words(path, word):
    pages = []
    word = word.lower()
    word_counter = 0

    with open(path, 'rb') as file:
        pdf = PdfReader(file)

        pages_in_document = len(pdf.pages)

        for i in range(pages_in_document):
            text = pdf.pages[i].extract_text()

            if not text:
                continue

            text = re.sub(r'[^a-zA-Zа-яA-ЯёЁ\s]', '', text.lower())
            text = text.split()


            count = text.count(word)

            if count > 0:
                pages.append(i)

                word_counter += count
    print(pages, word_counter)
    return pages, word_counter


def show_text(path, page):
    with open(path, 'rb') as file:
        pdf = PdfReader(file)

        text = pdf.pages[page]

        return text.extract_text()


