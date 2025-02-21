import os
from flask import Blueprint, render_template, request, Response
from marketplace_scraper import run_scraper

main = Blueprint('main', __name__)

KEYWORDS_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "keywords.py")

def load_keywords():
    keywords = {}
    with open(KEYWORDS_FILE_PATH, encoding="utf-8") as f:
        exec(f.read(), {}, keywords) #TODO: convert keywords to json
    return keywords

def save_keywords(keywords):
    with open(KEYWORDS_FILE_PATH, 'w', encoding="utf-8") as f:
        f.write("words = {\n")
        for key, value in keywords['words'].items():
            if value is None:
                f.write(f'"{key}": None,\n')
            else:
                f.write(f'"{key}": {value},\n')
        f.write("}\n")

@main.route('/', methods=['GET', 'POST'])
def home():
    keywords = load_keywords()

    return render_template('index.html', words=keywords['words'])

@main.route('/add', methods=['POST'])
def add_word():
    keywords = load_keywords()

    word = request.form['word']
    number_value = request.form['number_value']

    if word:
        if number_value.strip() == '':
            # i.e No limit
            keywords['words'][word] = None
        elif number_value.isdigit():
            keywords['words'][word] = int(number_value)

        save_keywords(keywords)

    return render_template('keywords_list.html', words=keywords['words'])

@main.route('/delete', methods=['POST'])
def delete_word():
    keywords = load_keywords()

    word_to_delete = request.form['word']
    if word_to_delete in keywords['words']:
        del keywords['words'][word_to_delete]
        save_keywords(keywords)

    return render_template('keywords_list.html', words=keywords['words'])

@main.route('/edit', methods=['POST'])
def edit_word():
    keywords = load_keywords()

    word_to_edit = request.form['word']
    new_price = request.form['new_price']

    if word_to_edit in keywords['words']:
        if new_price.strip() == '':
            # i.e No limit
            keywords['words'][word_to_edit] = None
        elif new_price.isdigit():
            keywords['words'][word_to_edit] = int(new_price)
        save_keywords(keywords)

    return render_template('keywords_list.html', words=keywords['words'])

@main.route('/scrape', methods=['GET'])
def scrape():
    def event_stream():
        yield "data: connection_established\n\n"
        for message in run_scraper():
            yield message

    return Response(event_stream(), mimetype='text/event-stream')
