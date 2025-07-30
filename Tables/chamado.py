from sqlalchemy import Column, Integer, String, Date, Text
from DB.database import Base

class Chamado(Base):
    __tablename__ = 'chamado'
    
    id = Column(Integer, primary_key=True)
    id_funcionario = Column(String(200))
    id_maquina = Column(Integer)
    categoria = Column(String(200))
    data_abertura = Column(Date)
    data_fechamento = (Column(Date))
    problema = Column(Text)
    fechamento = Column(String(200))

    