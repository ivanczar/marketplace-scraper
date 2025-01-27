from flask import Blueprint, render_template, request, redirect, url_for
import os

main = Blueprint('main', __name__)

keywords_file = os.path.join(os.getcwd(), './config', 'keywords.py')

def load_keywords():
    """Read the list of keywords from the db"""
    keywords = {}
    with open(keywords_file) as f:
        exec(f.read(), {}, keywords)
    return keywords

def save_keywords(keywords):
    """Save the keyword to db"""
    with open(keywords_file, 'w') as f:
        f.write("words = {\n")
        for key, value in keywords['words'].items():
            if value is None:
                f.write(f'"{key}": None,\n')
            else:
                f.write(f'"{key}": {value},\n')
        f.write("}\n")


@main.route('/', methods=['GET', 'POST'])
def home():
    """Render the homepage"""
    keywords = load_keywords()

    return render_template('index.html', words=keywords['words'])

@main.route('/add', methods=['POST'])
def add_word():
    """Add a keyword"""
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
    """Delete a keyword"""
    keywords = load_keywords()

    word_to_delete = request.form['word']
    if word_to_delete in keywords['words']:
        del keywords['words'][word_to_delete]
        save_keywords(keywords)

    return redirect(url_for('main.home'))

@main.route('/edit', methods=['POST'])
def edit_word():
    """Update the price of the keyword"""
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
