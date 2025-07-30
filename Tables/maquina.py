from sqlalchemy import Column, Integer, String
from DB.database import Base

class Maquina(Base):
    __tablename__ = 'maquina'
    
    id = Column(Integer, primary_key=True)
    nome_maquina = Column(String(200))
    setor = Column(String(200))


    