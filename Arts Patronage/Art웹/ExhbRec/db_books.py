from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Books(Base):
    __tablename__ = 'books_info'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    author = Column(String())
    text = Column(String())
    image = Column(String())
    genre = Column(String())
    noun = Column(String())

    def __init__(self, id=None, name=None, author=None, text=None, image=None, genre=None, noun=None ):
        self.id = id
        self.name = name
        self.author = author
        self.text = text
        self.image = image
        self.genre = genre
        self.noun = noun

    def __repr__(self):
        return "<T Books(id='%s', name='%s', author='%s', text='%s', image='%s', genre='%s', noun='%s')>" \
               % (self.id, self.name, self.author, self.text, self.image, self.genre, self.noun)
