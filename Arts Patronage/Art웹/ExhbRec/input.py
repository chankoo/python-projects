import pandas as pd

def art_input():
    western_data = pd.read_csv('static/data/western_preprocessed.csv')
    famous_paint = western_data[['title', 'artist', 'image']].sample(25)
    return famous_paint