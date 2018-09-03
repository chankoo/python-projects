from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from db_team import Base, Team
from db_arthub import Base, Arthub
from db_books import Base, Books
from flask_sqlalchemy import SQLAlchemy
from input import art_input
import pandas as pd
import input_book


from arthub_d2v import western_data
from arthub_d2v import lda_sim
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ExhbnRec.db'
app.config['SECRET_KEY'] = "dubu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = sqlite3.connect("ExhbnRec.db")
cur = conn.cursor()
data_final = pd.read_sql_query('SELECT * FROM arthub_info', conn)
book_list = pd.read_sql_query('SELECT name FROM books_info', conn)
book_name_list = book_list.name.tolist()
bestseller = []
ko_bestseller = db.session.query(Books).filter_by(genre="한국소설").limit(5).all()
jp_bestseller = db.session.query(Books).filter_by(genre="일본소설").limit(5).all()
en_bestseller = db.session.query(Books).filter_by(genre="영미소설").limit(5).all()
etc_bestseller = db.session.query(Books).filter_by(genre="기타 외국 소설").limit(5).all()
bestseller = [ko_bestseller, jp_bestseller, en_bestseller, etc_bestseller]



@app.route('/index_art')
def index_art():
    return render_template('index.html', famous_paint=art_input(), active='index_art')


@app.route('/')
def index():
    return render_template('index_book.html', active='index_book', book_list = book_name_list, bestseller=bestseller)


@app.route('/load_ajax', methods=["POST"])
def load_ajax():
    if request.method == "POST":
        book_name=request.form['book_name']
        result = db.session.query(Books).filter_by(name=book_name)

        book_nouns = None
        for row in result:
            book_nouns = row.noun.split(',')
        plot_url = input_book.word_cloud(book_nouns)
        return json.dumps({'status': 'OK', 'plot_url': plot_url})


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        book_name = request.args.get('book_name')  # 책 제목을 받음
        if book_name:
            book_info = db.session.query(Books).filter(Books.name==book_name).first()
        else:
            book_info = ""

    return render_template('index_book.html', active='index_book', book_name=book_name, book_info=book_info, book_list=book_name_list, bestseller=bestseller)


@app.route('/exhbnRec', methods = ['POST','GET']) # Exhibition Recommendation
def exhbnRec():
    test_txt_list = []

    title = ''
    try:
        title = request.form['title']
    except:
        pass

    if title != '':
        book_corpus = db.session.query(Books.noun).filter_by(name=title).first()
        sims = lda_sim(book_corpus, data_final)

    elif title=='':
        result = request.form
        result_selected = []

        for key in result.keys():
            if result[key] == '1':
                result_selected.extend(key)

        if not result_selected:
            return redirect(url_for('index_art'))

        for index in result_selected:
            test_txt_list.append(western_data['noun'][int(index)])

        test_txt_list = test_txt_list[0].split(',')

        sims = lda_sim(test_txt_list, data_final)
    else:
        return render_template('index_book.html', bestseller=bestseller, book_name_list=book_name_list, active='index_book')

    simsKeys = list(sims.keys())

    q = db.session.query(Arthub).filter(Arthub.id.in_(simsKeys))
    query_as_string = str(q.statement.compile(compile_kwargs={"literal_binds": True}))
    model=db.session.execute(query_as_string).fetchall()

    simsVal = []
    sorted_sims = sorted(sims.items(), key=lambda kv: kv[1], reverse=True)
    for tpl in sorted_sims:
        simsVal.append(tpl[1])

    return render_template('exhbnRec.html', active='exhbnRec', sims=simsVal, model=model)


@app.route('/aboutUs')  # about Us
def aboutUs():
    model = db.session.query(Team).all()
    return render_template('aboutUs.html', active='aboutUs', model=model)


@app.route('/intro')  # introduce
def intro():
    return render_template('intro.html', active='intro')


@app.route('/skills')  # Common Elements
def skills():
    return render_template('skills.html', active='skills')


@app.route('/elements')  # Common Elements
def elements():
    return render_template('elements.html', active='elements')


if __name__ == '__main__':
    app.run()

