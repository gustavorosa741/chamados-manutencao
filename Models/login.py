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

            if not usuario or not senha:
                self.error_text.value = "Preencha todos os campos!"
                page.update()
                return

            try:
                usuario_db = session.query(Usuario).filter_by(usuario=usuario).first()
                if usuario_db and check_password_hash(usuario_db.senha, senha):
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
                
                ft.OutlinedButton(
                    "Novo Usuário",
                    on_click=lambda e: self.novo_usuario(page),
                    icon=ft.Icons.PERSON_ADD,
                    width=300,
                    height=50
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

    def novo_usuario(self, page: ft.Page):
        import time
        page.window.maximized = True
        page.title = "Novo Usuário"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Poppins")
        aviso = ft.Text("", color=ft.Colors.RED, size=18)

        usuario = ft.TextField(
            label="Usuário",
            hint_text="Digite seu nome de usuário",
            width=300,
            border_radius=10,
            prefix_icon=ft.Icons.PERSON
        )

        senha = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        confirmar_senha = ft.TextField(
            label="Confirme sua senha",
            hint_text="Digite sua senha",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=10,
            prefix_icon=ft.Icons.LOCK
        )

        def voltar(e):
            self.__init__(page)
            page.update()

        def cadastrar(e):
            if not all([usuario.value, senha.value, confirmar_senha.value]):
                aviso.value = "Preencha todos os campos"
                aviso.color = ft.Colors.RED
                page.update()
                return

            if len(senha.value) < 8:
                aviso.value = "A senha deve ter no mínimo 8 caracteres"
                aviso.color = ft.Colors.RED
                page.update()
                return

            if senha.value != confirmar_senha.value:
                aviso.value = "As senhas não são iguais"
                aviso.color = ft.Colors.RED
                page.update()
                return

            verificar_usuario = session.query(Usuario).filter_by(usuario=usuario.value).first()
            try:
                if verificar_usuario:
                    aviso.value = "Usuário já existe"
                    aviso.color = ft.Colors.RED
                    page.update()
                    return

                novo_usuario = Usuario(usuario=usuario.value, senha=generate_password_hash(senha.value))
                session.add(novo_usuario)
                session.commit()

                aviso.value = "Usuário cadastrado com sucesso"
                aviso.color = ft.Colors.GREEN
                page.update()
                time.sleep(1)
                self.__init__(page)

            except Exception as ex:
                aviso.value = f"Erro: {str(ex)}"
                aviso.color = ft.Colors.RED
                page.update()

        login_form = ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=ft.Colors.TEAL),
                ft.Text("Novo Usuário", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                usuario,
                senha,
                confirmar_senha,
                aviso,
                ft.Container(
                    ft.ElevatedButton(
                        "Cadastrar",
                        on_click=cadastrar,
                        icon=ft.Icons.ADD,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20,
                            bgcolor=ft.Colors.TEAL_400,
                            color=ft.Colors.WHITE
                        ),
                        width=300,
                        height=50
                    ),
                    margin=ft.margin.only(top=20)
                ),

                ft.TextButton(
                    "Voltar",
                    on_click=voltar,
                    icon=ft.Icons.ARROW_BACK,
                    style=ft.ButtonStyle(color=ft.Colors.RED)
                )
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
                        content=login_form,
                        padding=40,
                        width=500,
                        border_radius=20,
                        bgcolor=ft.Colors.WHITE,
                    ),
                    elevation=10,
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.Colors.GREY_200
            )
        )

            

