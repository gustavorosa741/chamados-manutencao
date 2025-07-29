from sqlalchemy import Column, Integer, String
from DB.database import Base
from werkzeug.security import generate_password_hash

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    senha = Column(String(200), nullable=False)
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
