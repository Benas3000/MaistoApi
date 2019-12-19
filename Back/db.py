from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Maistas(Base):
    __tablename__ = "maistas"

    id = Column('id', Integer, primary_key=True)
    pavadinimas = Column('pavadinimas', String)
    kcal = Column('kcal', Integer)
    angliavandeniai = Column('anglevandeniai', Integer)
    riebalai = Column('riebalai', Integer)
    sotiejiRiebalai = Column('sotiejiRiebalai', Integer)
    baltymai = Column('baltymai', Integer)
    kokybe = Column('kokybe', Integer)
    


engine = create_engine('sqlite:///:maistoDb:', echo=True)
#Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)