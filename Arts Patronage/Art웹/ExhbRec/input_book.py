import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import platform
import io
import base64
import sqlite3

conn = sqlite3.connect("ExhbnRec.db")
cur = conn.cursor()
data_final = pd.read_sql_query('SELECT * FROM arthub_info', conn)
book_list = pd.read_sql_query('SELECT name FROM books_info', conn)
book_name_list = book_list.name.tolist()


def word_cloud(book_nouns):
    img = io.BytesIO()

    # OS별 matplotlib 한국어 처리
    path = "static/AppleGothic.ttf"  # window 사용자의 경우 path 설정 중요
    from matplotlib import font_manager, rc
    if platform.system() == 'Darwin':
        rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)
    else:
        print('Unknown system... sorry~~~~')

    # 워드 클라우드 만들기 시작

    with open('static/data/project_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().split(' ')
    book_nouns = [each_word for each_word in book_nouns if each_word not in stop_words]

    counts_nouns = Counter(book_nouns)  # ##book_nouns리스트를 카운트된 딕셔너리로 바꿈

    # for win : font_path='c:/Windows/Fonts/malgun.ttf'
    try:
        wordcloud = WordCloud(font_path='static/AppleGothic.ttf',
                          relative_scaling=0.2,
                          background_color='white'
                          , max_words=150).generate_from_frequencies(counts_nouns)
    except Exception as e:
        print(e)
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()
