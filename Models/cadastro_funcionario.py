import flet as ft
from DB.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from Tables.usuario import Usuario
    

class CadastroUsuario:
    def __init__(self):

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

        self.error_text = ft.Text("", size=18)

        def cadastrar_user(e):
            if not all([usuario.value, senha.value, confirmar_senha.value]):
                self.error_text.value = "Preencha todos os campos!"
                self.error_text.color = ft.Colors.RED
                e.page.update()

            elif len(senha.value) < 8:
                self.error_text.value = "A senha deve ter no mínimo 8 caracteres"
                self.error_text.color = ft.Colors.RED
                e.page.update()

            elif senha.value != confirmar_senha.value:
                self.error_text.value = "As senhas não são iguais"
                self.error_text.color = ft.Colors.RED
                e.page.update()
                return
                
            verificar_usuario = session.query(Usuario).filter_by(usuario=usuario.value).first()

            try:
                if verificar_usuario:
                    self.error_text.value = "Usuário já existe"
                    self.error_text.color = ft.Colors.RED
                    e.page.update()
                    return

                novo_usuario = Usuario(usuario=usuario.value, senha=generate_password_hash(senha.value))
                session.add(novo_usuario)
                session.commit()

                self.error_text.value = "Usuário cadastrado com sucesso"
                self.error_text.color = ft.Colors.GREEN
                e.page.update()
            
            except Exception as ex:
                self.error_text.value = f"Erro: {str(ex)}"
                self.error_text.color = ft.Colors.RED
                e.page.update()

                

        self.login_form = ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=50, color=ft.Colors.TEAL),
                ft.Text("Novo Usuário", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                usuario,
                senha,
                confirmar_senha,
                self.error_text,
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


            

