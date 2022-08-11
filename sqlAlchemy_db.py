import sqlalchemy.types
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.databases import postgres
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
import psycopg2

engine = create_engine('postgresql://otojieihxizijz:8aa3d812701ffa71cebc9cad575daab25520cdb309711d3266bb9a67159ff034@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d4ps43fkmtvvam', echo=True)

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


