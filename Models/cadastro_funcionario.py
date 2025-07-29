import flet as ft
from DB.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from Tables.usuario import Usuario
    


class CadastroUsuario:
    def __init__(self):
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

        def cadastrar_user(e):
            if not all([usuario.value, senha.value, confirmar_senha.value]):
                aviso.value = "Preencha todos os campos"
                aviso.color = ft.Colors.RED
                
                return

            if len(senha.value) < 8:
                aviso.value = "A senha deve ter no mínimo 8 caracteres"
                aviso.color = ft.Colors.RED
                
                return

            if senha.value != confirmar_senha.value:
                aviso.value = "As senhas não são iguais"
                aviso.color = ft.Colors.RED
                
                return

            verificar_usuario = session.query(Usuario).filter_by(usuario=usuario.value).first()
            try:
                if verificar_usuario:
                    aviso.value = "Usuário já existe"
                    aviso.color = ft.Colors.RED
                    
                    return

                novo_usuario = Usuario(usuario=usuario.value, senha=generate_password_hash(senha.value))
                session.add(novo_usuario)
                session.commit()

                aviso.value = "Usuário cadastrado com sucesso"
                aviso.color = ft.Colors.GREEN

            except Exception as ex:
                aviso.value = f"Erro: {str(ex)}"
                aviso.color = ft.Colors.RED

        self.login_form = ft.Column(
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
                        on_click=cadastrar_user,
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.login_form,
                    padding=40,
                    width=900,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE,
                ),
                elevation=10,
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.BLUE_100
        )


            

