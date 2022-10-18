import sqlalchemy.types
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.databases import mysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects
import psycopg2

engine = create_engine('sqlite:///db.sqlite3', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'usuarios'

    idsuario = Column( Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(100))
    apelido = Column(String(50))
    senha = Column(String(300))
    tipo = Column(String(50))

    def __repr__(self):
        return f'User {self.name}'


class Aviso(Base):
    __tablename__ = 'aviso'

    idaviso = Column( Integer, primary_key=True, autoincrement=True )
    data = Column(String(1000))
    problema = Column( String(1000) )
    descricao = Column( String(1000) )


Base.metadata.create_all(engine)


