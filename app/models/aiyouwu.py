from sqlalchemy import Column, String, Integer, orm

from app.models.base import Base



class Aiyouwu(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    ori_url = Column(String(255))
    local_url = Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'ori_url', 'local_url']


