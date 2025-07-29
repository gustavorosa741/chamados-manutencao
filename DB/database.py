from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

usuario = os.getenv("USUARIO")
senha = os.getenv("SENHA")

engine = create_engine(f"mysql+pymysql://{usuario}:{senha}@localhost:3306/chamados")

#engine = create_engine(f"sqlite:///{Path(__file__).parent}/biblioteca.db")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()