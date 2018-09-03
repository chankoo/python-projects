from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Team(Base):
    __tablename__ = 'team_info'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    role = Column(String())
    etc = Column(String())
    photoUrl = Column(String())

    def __init__(self, id=None, name=None, role=None, etc=None, photoUrl=None):
        self.id = id
        self.name = name
        self.role = role
        self.etc = etc
        self.photoUrl = photoUrl

    def __repr__(self):
        return "<T Team(id='%s',name='%s',role='%s',etc='%s',photoUrl='%s' )>" \
               % (self.id, self.name, self.role, self.etc, self.photoUrl)
