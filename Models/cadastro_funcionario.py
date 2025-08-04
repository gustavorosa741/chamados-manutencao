import flet as ft
from DB.database import session
from werkzeug.security import generate_password_hash, check_password_hash
from Tables.usuario import Usuario
from sqlalchemy import or_


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
            try:
                verificar_usuario = session.query(Usuario).filter_by(usuario=usuario.value).first()

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

                elif verificar_usuario:
                    self.error_text.value = "Usuário já existe"
                    self.error_text.color = ft.Colors.RED
                    e.page.update()
                else:
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
                    width=500,
                    height=600,
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
    
class ListarUsuario:
    def __init__(self, page: ft.Page):
        self.texto_aviso = ft.Text("", size=18)
        self.page = page
        self.dialog = ft.AlertDialog(modal=True)
        
        self.barra_pesquisa = ft.SearchBar(
            bar_hint_text="Pesquise por nome",
            on_change=self.filtrar_usuario,
            on_submit=self.filtrar_usuario,
            width=250,
            height=40,
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome da Usuário")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.BLACK),
            heading_row_color=ft.Colors.BLUE_100,
            data_row_color=ft.Colors.WHITE,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
        )

        self.formulario = ft.Column(
            [
                ft.Text("Lista de Usuários", size=28, weight=ft.FontWeight.BOLD),
                ft.Row([self.barra_pesquisa], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    content=self.tabela,
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    expand=True
                ),
                self.texto_aviso,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            scroll=ft.ScrollMode.AUTO
        )

        self.atualizar_tabela()

    def gerar_linha_tabela(self, usuario: Usuario):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(usuario.usuario)),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip= "Editar",
                                on_click=lambda e, usuario=usuario: self.editar_usuario(usuario)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip= "Excluir",
                                on_click=lambda e, usuario=usuario: self.excluir_usuario(usuario)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            ]
        )
    
    def fechar_dialogo(self):
        self.dialog.open = False
        self.dialog.update()

    def editar_usuario(self, usuario: Usuario):
        self.dialog.title = ft.Text(f"Editando: {usuario.usuario}")
        self.dialog.content = ft.Column(
            [
                ft.TextField(label="Nome", value=usuario.usuario),
                ft.TextField(label="Senha"),
                ft.TextField(label="Confirmar Senha"),
            ],
            spacing=5,
        )
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
            ft.TextButton("Salvar", on_click=lambda e: self.salvar_edicao(usuario)),
        ]
        self.page.open(self.dialog)
        self.dialog.update()
    
    def salvar_edicao(self, usuario: Usuario):
        try:
            if not all([self.dialog.content.controls[0].value, self.dialog.content.controls[1].value, self.dialog.content.controls[2].value,]):
                self.dialog.title = ft.Text("Erro", color=ft.Colors.RED)
                self.dialog.content = ft.Text("Preencha todos os campos", size=18, color=ft.Colors.RED)
                self.dialog.actions = [
                    ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo()),
                    ]
                self.page.open(self.dialog)
                self.dialog.update()

            elif len(self.dialog.content.controls[1].value) < 8:
                self.dialog.title = ft.Text("Erro", color=ft.Colors.RED)
                self.dialog.content = ft.Text("A senha precisa ter no minimo 8 caracteres", size=18, color=ft.Colors.RED)
                self.dialog.actions = [
                    ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo()),
                    ]
                self.page.open(self.dialog)
                self.dialog.update()

            elif self.dialog.content.controls[2].value != self.dialog.content.controls[1].value:
                self.dialog.title = ft.Text("Erro", color=ft.Colors.RED)
                self.dialog.content = ft.Text("As senhas não são iguais", size=18, color=ft.Colors.RED)
                self.dialog.actions = [
                    ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo()),
                    ]
                self.page.open(self.dialog)
                self.dialog.update()

            else:
                usuario.usuario = self.dialog.content.controls[0].value
                usuario.senha = generate_password_hash(self.dialog.content.controls[1].value)
                session.commit()
                
                self.dialog.title = ft.Text("Sucesso", color=ft.Colors.GREEN)
                self.dialog.content = ft.Text("Usuario alterado com sucesso!", size=18, color=ft.Colors.GREEN)
                self.dialog.actions = [
                    ft.TextButton("OK", on_click=lambda e: self.fechar_dialogo()),
                    ]
                self.page.open(self.dialog)
                self.dialog.update()

                self.atualizar_tabela()
                self.page.update()

        except Exception as e:
            session.rollback()
            self.texto_aviso.value = f"Erro: {str(e)}"
            self.texto_aviso.color = ft.Colors.RED

            self.page.close(self.dialog)
            self.page.update()
        
    def excluir_usuario(self, usuario: Usuario):
        self.dialog.title = ft.Text(f"Excluir: {usuario.usuario}")
        self.dialog.content = ft.Text("Deseja excluir este usuário?")
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=self.fechar_dialogo),
            ft.TextButton("Excluir", on_click=lambda e: self.confirmar_exclusao(usuario)),
        ]
        self.page.open(self.dialog)
        self.dialog.update()

    def confirmar_exclusao(self, usuario: Usuario):
        try:
            session.delete(usuario)
            session.commit()
            self.fechar_dialogo()
        except Exception as e:
            session.rollback()
            self.texto_aviso.value = f"Erro: {str(e)}"
            self.texto_aviso.color = ft.Colors.RED

        self.page.close(self.dialog)
        self.atualizar_tabela()
        self.page.update()


    def filtrar_usuario(self, e):
        try:
            busca = self.barra_pesquisa.value.upper()

            query = session.query(Usuario)

            if busca:
                query = query.filter(
                    or_(
                        Usuario.usuario.ilike(f"%{busca}%"),
                    )
                
                )
        
            usuarios = query.all()

            self.tabela.rows = [self.gerar_linha_tabela(usuario) for usuario in usuarios]

            self.texto_aviso.value = f"{len(usuarios)} Usuários encontrados"
            self.texto_aviso.color = ft.Colors.GREEN

            if not usuarios:
                self.texto_aviso.value = "Nenhuma usuário encontrado"
                self.texto_aviso.color = ft.Colors.RED
                return
        
        except Exception as ex:
            self.texto_aviso.value = f"Erro: {str(ex)}"
            self.texto_aviso.color = ft.Colors.RED
            self.page.update()
        
        self.page.update()

    def atualizar_tabela(self):
        try:
            busca = self.barra_pesquisa.value.upper()

            usuarios = session.query(Usuario).filter(Usuario.usuario.like(f"%{busca}%")).all()
            self.tabela.rows.clear()

            for usuario in usuarios:
                self.tabela.rows.append(self.gerar_linha_tabela(usuario))

            if not usuarios:
                self.texto_aviso.value = "Nenhuma usuário encontrado"
                self.texto_aviso.color = ft.Colors.RED
            else:
                self.texto_aviso.value = f"{len(usuarios)} usuários encontrados"
                self.texto_aviso.color = ft.Colors.GREEN

            self.page.update()

        except Exception as ex:
            self.texto_aviso.value = f"Erro: {str(ex)}"
            self.texto_aviso.color = ft.Colors.RED
            self.page.update()

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
                    padding=40,
                    width=600,
                    height=600,
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
    
    
