from operator import or_
import flet as ft
from DB.database import session
from Tables.aluno import Aluno



def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()

class CadastroAluno:
    def __init__(self):
        self.nome = ft.TextField(
            label="Nome do Aluno",
            hint_text="Digite o nome completo",
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.idade = ft.TextField(
            label="Idade",
            hint_text="Ex: 14",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.turma = ft.TextField(
            label="Turma",
            hint_text="Ex: 8ºA",
            prefix_icon=ft.Icons.GROUP,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            width=400,
            on_change=formatacao
        )

        self.status_texto = ft.Text("", size=18)

        self.botao_cadastrar = ft.ElevatedButton(
            text="Cadastrar",
            icon=ft.Icons.CHECK_CIRCLE,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
            ),
            width=400,
            height=50,
            on_click=self.cadastrar_aluno
        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Aluno", size=32, weight=ft.FontWeight.BOLD),
                self.nome,
                self.idade,
                self.turma,
                self.botao_cadastrar,
                self.status_texto,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
    def cadastrar_aluno(self, e: ft.ControlEvent):
        nome = self.nome.value
        idade = int(self.idade.value) if self.idade.value.isdigit() else None
        turma = self.turma.value

        buscar_aluno = session.query(Aluno).filter(Aluno.nome == nome).first()
        
        if not nome or not idade or not turma:
            self.status_texto.value = "Preencha todos os campos corretamente!"
            self.status_texto.color = ft.Colors.RED

        elif idade <0 or idade > 120:
            self.status_texto.value = "Idade inválida!"
            self.status_texto.color = ft.Colors.RED

        elif buscar_aluno:
            self.status_texto.value = "Aluno já cadastrado!"
            self.status_texto.color = ft.Colors.RED

        else:
            novo_aluno = Aluno(nome=nome, idade=idade, turma=turma)
            session.add(novo_aluno)
            session.commit()
            self.status_texto.value = "Aluno cadastrado com sucesso!"
            self.status_texto.color = ft.Colors.GREEN

        e.page.update()

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
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
            bgcolor=ft.Colors.BLUE_100
        )

class ListaAlunos:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_texto = ft.Text("", size=18)
        self.dialog = ft.AlertDialog(modal=True)

        self.barra_pesquisa = ft.SearchBar(
            bar_hint_text="Pesquisar por nome, turma ou idade",
            on_change= self.filtrar_alunos,
            on_submit=self.filtrar_alunos,
            width=400,
            height=50,
        )

        self.tabela_alunos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Idade")),
                ft.DataColumn(ft.Text("Turma")),
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
                ft.Text("📚 Lista de Alunos", size=28, weight=ft.FontWeight.BOLD),
                ft.Row([self.barra_pesquisa], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    content=self.tabela_alunos,
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    expand=True
                ),
                self.status_texto,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            scroll=ft.ScrollMode.AUTO
        )

        self.atualizar_lista()

    def gerar_linha_tabela(self, aluno: Aluno):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(aluno.id))),
                ft.DataCell(ft.Text(aluno.nome)),
                ft.DataCell(ft.Text(str(aluno.idade))),
                ft.DataCell(ft.Text(aluno.turma)),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Aluno",
                                on_click=lambda e, aluno=aluno: self.editar_aluno(aluno)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Excluir Aluno",
                                on_click=lambda e, aluno=aluno: self.excluir_aluno(aluno)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
            ]
        )
    
    def fechar_dialogo(self):
        self.dialog.open = False
        self.page.update()
    
    def editar_aluno(self, aluno: Aluno):
        self.dialog.title = ft.Text(f"Editando: {aluno.nome}")
        self.dialog.content = ft.Column(
            [
                    ft.TextField(label="Nome", value=aluno.nome, on_change=formatacao),
                    ft.TextField(label="Idade", value=int(aluno.idade), on_change=formatacao),
                    ft.TextField(label="Turma", value=aluno.turma, on_change=formatacao),
            ],
            spacing=5
        )
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
            ft.TextButton("Salvar", on_click=lambda e: self.confirmar_edicao(aluno))
        ]
        self.page.open(self.dialog)
        self.page.update()

    def confirmar_edicao(self, aluno: Aluno):
        try:
            aluno.nome = self.dialog.content.controls[0].value
            aluno.idade = int(self.dialog.content.controls[1].value)
            aluno.turma = self.dialog.content.controls[2].value
            
            session.commit()
            self.status_texto.value = "Aluno editado com sucesso!"
            self.status_texto.color = ft.Colors.GREEN
        except ValueError:
            self.status_texto.value = "Idade deve ser um número válido!"
            self.status_texto.color = ft.Colors.RED
        except Exception as e:
            session.rollback()
            self.status_texto.value = f"Erro: {str(e)}"
            self.status_texto.color = ft.Colors.RED
        
        self.page.close(self.dialog)
        self.atualizar_lista()
        self.page.update()

    def excluir_aluno(self, aluno: Aluno):
        self.dialog.title = ft.Text(f"Excluir Aluno: {aluno.nome}")
        self.dialog.content = ft.Text(f"Tem certeza que deseja excluir o aluno {aluno.nome}?")
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
            ft.TextButton("Excluir", on_click=lambda e: self.confirmar_exclusao(aluno))
        ]
        self.page.open(self.dialog)
        self.page.update()

    def confirmar_exclusao(self, aluno: Aluno):
        from Models.emprestimo import Emprestimo
        try:
            session.delete(aluno)
            session.commit()
            self.fechar_dialogo()
        except Exception as e:
            session.rollback()
            self.status_texto.value = f"Erro ao excluir aluno: {str(e)}"
            self.status_texto.color = ft.Colors.RED
            
        self.atualizar_lista()
        self.page.update()

    def filtrar_alunos(self, e):
        termo_busca = self.barra_pesquisa.value.strip().lower() if self.barra_pesquisa.value else ""

        query = session.query(Aluno)

        if termo_busca:
            try:
                idade_busca = int(termo_busca)
                query = query.filter(
                    or_(
                        or_(
                            Aluno.nome.ilike(f"%{termo_busca}%"),
                            Aluno.turma.ilike(f"%{termo_busca}%")
                        ),
                        Aluno.idade == idade_busca
                    )
                )
            except ValueError:
                query = query.filter(
                    or_(
                        Aluno.nome.ilike(f"%{termo_busca}%"),
                        Aluno.turma.ilike(f"%{termo_busca}%")
                    )
                )

        alunos_filtrados = query.all()

        self.tabela_alunos.rows = [
            self.gerar_linha_tabela(aluno)
            for aluno in alunos_filtrados
        ]

        self.status_texto.value = (
            "Nenhum aluno encontrado." if not alunos_filtrados 
            else f"{len(alunos_filtrados)} aluno(s) encontrado(s)."
        )
        self.status_texto.color = (
            ft.Colors.RED if not alunos_filtrados 
            else ft.Colors.GREEN
        )

        if e is not None:
            self.page.update()
            
    def atualizar_lista(self):
        self.filtrar_alunos(None)
        alunos = session.query(Aluno).all()
        self.tabela_alunos.rows.clear()

        for aluno in alunos:
            self.tabela_alunos.rows.append(self.gerar_linha_tabela(aluno))

        if not alunos:
            self.status_texto.value = "Nenhum aluno cadastrado."
            self.status_texto.color = ft.Colors.RED

        else:
            self.status_texto.value = f"{len(alunos)} aluno(s) cadastrado(s)."
            self.status_texto.color = ft.Colors.GREEN

        self.page.update()
            
    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
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