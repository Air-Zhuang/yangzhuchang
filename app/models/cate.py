from sqlalchemy import Column, String, Integer, orm

from app.models.base import Base



class Cate(Base):
    id = Column(Integer, primary_key=True)
    cate_name=Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'cate_name']



