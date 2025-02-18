import os
from flask import Blueprint, render_template, request, redirect, url_for, Response
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

    if request.method == 'POST':
        word = request.form['word']
        number_value = request.form['number_value']

        if word and number_value.isdigit():
            keywords['words'][word] = int(number_value)
            save_keywords(keywords)

    return redirect(url_for('main.home'))

@main.route('/delete', methods=['POST'])
def delete_word():
    keywords = load_keywords()

    word_to_delete = request.form['word']
    if word_to_delete in keywords['words']:
        del keywords['words'][word_to_delete]
        save_keywords(keywords)

    return redirect(url_for('main.home'))

@main.route('/edit', methods=['POST'])
def edit_word():
    keywords = load_keywords()

    word_to_edit = request.form['word']
    new_price = request.form['new_price']

    if word_to_edit in keywords['words']:
        if new_price.isdigit():
            keywords['words'][word_to_edit] = int(new_price)
        else:
            keywords['words'][word_to_edit] = None
        save_keywords(keywords)

    return redirect(url_for('main.home'))

@main.route('/scrape', methods=['GET'])
def scrape():
    return Response(run_scraper(), mimetype='text/event-stream')
