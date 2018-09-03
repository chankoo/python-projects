from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Arthub(Base):
    __tablename__ = 'arthub_info'
    id = Column(Integer(), primary_key=True)
    exhbn_title = Column(String())
    link = Column(String())
    exhbn_artist = Column(String())
    exhbn_schedule = Column(String())
    contect = Column(String())
    homepage = Column(String())
    text_content = Column(String())
    image_link = Column(String())
    topic = Column(String())

    def __init__(self, id=None, exhbn_title=None, link=None, exhbn_artist=None, exhbn_schedule=None, contect=None, homepage=None, text_content=None, image_link=None, topic=None ):
        self.id = id
        self.exhbn_title = exhbn_title
        self.link = link
        self.exhbn_artist = exhbn_artist
        self.exhbn_schedule = exhbn_schedule
        self.contect = contect
        self.homepage = homepage
        self.text_content = text_content
        self.image_link = image_link
        self.topic = topic

    def __repr__(self):
        return "<T Arthub(id='%s', exhbn_title='%s', link='%s', exhbn_artist='%s', exhbn_schedule='%s'," \
               " contect='%s', homepage='%s', text_content='%s', image_link='%s', topic='%s' )>" \
               % (self.id, self.exhbn_title, self.link, self.exhbn_artist, self.exhbn_schedule, self.contect, self.homepage, self.text_content, self.image_link, self.topic)
