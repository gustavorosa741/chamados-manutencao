import flet as ft
from DB.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from Tables.usuario import Usuario

class Login:
    def __init__(self, page: ft.Page):
        page.window.maximized = True
        page.title = "Login"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Poppins")

        self.username_field = ft.TextField(
            label="Usuário",
            hint_text="Digite seu nome de usuário",
            width=300,
            border_radius=10,
            prefix_icon=ft.Icons.PERSON
        )

        self.password_field = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        self.error_text = ft.Text("", color=ft.Colors.RED, size=18)

        def fechar_app(e):
            page.clean()
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.add(ft.Text("Aplicação fechada."))
            session.close()

        def logar(e):
            usuario = self.username_field.value
            senha = self.password_field.value

            try:
                usuario_db = session.query(Usuario).filter_by(usuario=usuario).first()

                if not usuario or not senha:
                    self.error_text.value = "Preencha todos os campos!"
                    page.update()

                elif usuario_db and check_password_hash(usuario_db.senha, senha):
                    from Models.menu_principal import MenuPrincipal
                    page.clean()
                    MenuPrincipal(page)
                    
                else:
                    self.error_text.value = "Usuário ou senha inválidos!"
                    page.update()

            except Exception as ex:
                self.error_text.value = f"Erro: {str(ex)}"
                page.update()

        conteudo = ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=ft.Colors.TEAL),
                ft.Text("Login", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                self.username_field,
                self.password_field,
                self.error_text,
                ft.Container(
                    ft.ElevatedButton(
                        "Entrar",
                        on_click=logar,
                        icon=ft.Icons.LOGIN,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20,
                            bgcolor=ft.Colors.TEAL_400,
                            color=ft.Colors.WHITE,
                        ),
                        width=300,
                        height=50
                    ),
                    margin=ft.margin.only(top=20)
                ),
                
                ft.TextButton(
                    "Fechar Aplicação",
                    on_click=fechar_app,
                    icon=ft.Icons.EXIT_TO_APP,
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                    width=200,
                    height=40
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=conteudo,
                        padding=40,
                        width=500,
                        height=600,
                        border_radius=20,
                        bgcolor=ft.Colors.WHITE70,
                    ),
                    elevation=10,
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.GREY_200
            )
        )

