import sqlalchemy.types
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://b6914c23389c6b:cd8edf81@us-cdbr-east-06.cleardb.net/heroku_a7f279a8e4d980e', echo=True)

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
    data = Column(sqlalchemy.types.DateTime)
    problema = Column( String(100) )
    descricao = Column( String(500) )


Base.metadata.create_all(engine)


