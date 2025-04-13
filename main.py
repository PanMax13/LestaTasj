from PyPDF2 import PdfReader
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from math import log

from logic import find_words, show_text, count_words, get_tf

app = FastAPI()

app.mount('/static', StaticFiles(directory='./static'), name='static')
template = Jinja2Templates(directory='templates')

@app.get('/')
async def main(request: Request):
    return template.TemplateResponse(request=request, name='form.html')


@app.post('/data')
async def upload_data(
        request: Request,
        files: List[UploadFile] = Form(...),
        searched_word: str = Form(...),
):
    form = await request.form()
    print(form)

    saved_files = []
    word = searched_word

    for file in files:
        filename = file.filename

        location = f'./files/{file.filename}'

        with open(location, 'wb') as file_location:
            file_location.write(file.file.read())

            saved_files.append(location)
    if len(saved_files) == 1:
        location = saved_files[0]
        pages, words = find_words(location, word)
        texts = []

        for page in pages:
            text = show_text(location, page)
            text = text.replace(word, f'<span>{word}</span>')

            texts.append(text)

        all_words = count_words(location)
        tf = get_tf(location, words)

        context = {
            'word': word,
            'filename': filename,
            'value': words,
            'texts': texts,
            'pages': pages,
            'tf': tf
        }

        return template.TemplateResponse(request=request, name='pages.html', context=context)

    else:
        true_words = []

        words = 0
        for file in saved_files:
            count = find_words(file, word)[1]
            words += count
            with open(file, 'rb') as file_:
                pdf = PdfReader(file_)
                full_text = ""

                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text.lower() + "\n"

                if word.lower() in full_text:
                    true_words.append(file)

        print(len(true_words))
        idf = log(len(files) / len(true_words))
        context = {
            'word': word,
            'value': words,
            'filename': saved_files,
            'idf': idf
        }

        return template.TemplateResponse(request=request, name='idf.html', context=context)