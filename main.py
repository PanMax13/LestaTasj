from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from logic import find_words, show_text

app = FastAPI()

app.mount('/static', StaticFiles(directory='./static'), name='static')
template = Jinja2Templates(directory='templates')

@app.get('/')
async def main(request: Request):
    return template.TemplateResponse(request=request, name='form.html')


@app.post('/data')
async def upload_data(
        request: Request,
        file: UploadFile = Form(...),
        searched_word: str = Form(...),
):

    filename = file.filename
    word = searched_word

    location = f'./files/{file.filename}'

    with open(location, 'wb') as file_location:
        file_location.write(file.file.read())

    pages, words = find_words(location, word)

    texts = []

    for page in pages:
        text = show_text(location, page)
        text = text.replace(word, f'<span>{word}</span>')

        texts.append(text)

    print(texts)

    context = {
        'word': word,
        'filename': filename,
        'value': words,
        'texts': texts,
        'pages': pages
    }

    return template.TemplateResponse(request=request, name='pages.html', context=context)
