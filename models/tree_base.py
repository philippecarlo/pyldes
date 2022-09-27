from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TreeBase():
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}