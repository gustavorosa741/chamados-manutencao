import flet as ft
from DB.database import engine, Base

def create_tables():
    Base.metadata.create_all(engine)

def main(page: ft.Page):
    create_tables()
    Login(page)
    page.update()

if __name__ == "__main__":
    #abrir app desktop
    ft.app(target=main)

    #abrir app navegador
    #ft.app(target=main, view=None, host="0.0.0.0", port=8080)