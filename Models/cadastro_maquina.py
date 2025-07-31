import flet as ft
from sqlalchemy import or_
from DB.database import session
from Tables.maquina import Maquina

def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()

class CadastroMaquina:
    def __init__(self):
        self.nome = ft.TextField(
            label="Nome da Máquina",
            hint_text="Digite o nome da máquina",
            width=350,
            border_radius=10,
            prefix_icon=ft.Icons.HARDWARE,
            on_change=formatacao,
        )
        
        self.setor = ft.TextField(
            label="Setor",
            hint_text="Digite o setor da máquina",
            width=350,
            border_radius=10,
            prefix_icon=ft.Icons.LOCATION_ON,
            on_change=formatacao,
        )
        
        self.texto_aviso = ft.Text("", size=18)

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
            on_click=self.cadastrar_maquina

        )

        self.formulario = ft.Column(
            [
                ft.Text("Cadastro de Máquina", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                self.nome,
                self.setor,
                self.texto_aviso,
                self.botao_cadastrar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ) 
    
  
        

    def cadastrar_maquina(self, e):
        nome = self.nome
        setor = self.setor

        try:
            busca_maquina = session.query(Maquina).filter_by(nome_maquina=nome.value).first()

            if not nome or not setor:
                self.texto_aviso.value = "Preencha todos os campos!"
                self.texto_aviso.color = ft.Colors.RED
                e.page.update()

            elif busca_maquina:
                self.texto_aviso.value = "Máquina já cadastrada"
                self.texto_aviso.color = ft.Colors.RED
                e.page.update()
            else:
                nova_maquina = Maquina(nome_maquina=nome.value, setor=setor.value)
                session.add(nova_maquina)
                session.commit()

                self.texto_aviso.value = "Máquina cadastrada com sucesso"
                self.texto_aviso.color = ft.Colors.GREEN
                e.page.update()

        except Exception as ex:
            self.texto_aviso.value = f"Erro: {str(ex)}"
            self.texto_aviso.color = ft.Colors.RED
            e.page.update()

    def get_container(self):
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=self.formulario,
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

class ListarMaquina:
    def __init__(self, page: ft.Page):
        self.texto_aviso = ft.Text("", size=18)
        self.page = page
        self.dialog = ft.AlertDialog(modal=True)
        
        self.barra_pesquisa = ft.SearchBar(
            bar_hint_text="Pesquise por nome ou setor",
            on_change=self.filtrar_maquina,
            on_submit=self.filtrar_maquina,
            width=250,
            height=40,
        )

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome da Máquina")),
                ft.DataColumn(ft.Text("Setor")),
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
                ft.Text("Lista de Maquinas", size=28, weight=ft.FontWeight.BOLD),
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

    def gerar_linha_tabela(self, maquina: Maquina):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(maquina.nome_maquina)),
                ft.DataCell(ft.Text(maquina.setor)),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip= "Editar",
                                on_click=lambda e, maquina=maquina: self.editar_maquina(maquina)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip= "Excluir",
                                on_click=lambda e, maquina=maquina: self.excluir_maquina(maquina)
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

    def editar_maquina(self, maquina: Maquina):
        self.dialog.title = ft.Text(f"Editando: {maquina.nome_maquina}")
        self.dialog.content = ft.Column(
            [
                ft.TextField(label="Nome", value=maquina.nome_maquina, on_change=formatacao),
                ft.TextField(label="Setor", value=maquina.setor, on_change=formatacao),
            ],
            spacing=5,
        )
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
            ft.TextButton("Salvar", on_click=lambda e: self.salvar_edicao(maquina)),
        ]
        self.page.open(self.dialog)
        self.dialog.update()
    
    def salvar_edicao(self, maquina: Maquina):
        try:
            maquina.nome_maquina = self.dialog.content.controls[0].value
            maquina.setor = self.dialog.content.controls[1].value
            session.commit()
            
            self.texto_aviso.value = "Máquina editada com sucesso"
            self.texto_aviso.color = ft.Colors.GREEN

        except Exception as e:
            session.rollback()
            self.texto_aviso.value = f"Erro: {str(e)}"
            self.texto_aviso.color = ft.Colors.RED

        self.page.close(self.dialog)
        self.atualizar_tabela()
        self.page.update()
        
    def excluir_maquina(self, maquina: Maquina):
        self.dialog.title = ft.Text(f"Excluir: {maquina.nome_maquina}")
        self.dialog.content = ft.Text("Deseja excluir esta máquina?")
        self.dialog.actions = [
            ft.TextButton("Cancelar", on_click=self.fechar_dialogo),
            ft.TextButton("Excluir", on_click=lambda e: self.confirmar_exclusao(maquina)),
        ]
        self.page.open(self.dialog)
        self.dialog.update()

    def confirmar_exclusao(self, maquina: Maquina):
        try:
            session.delete(maquina)
            session.commit()
            self.fechar_dialogo()
        except Exception as e:
            session.rollback()
            self.texto_aviso.value = f"Erro: {str(e)}"
            self.texto_aviso.color = ft.Colors.RED

        self.page.close(self.dialog)
        self.atualizar_tabela()
        self.page.update()

    def filtrar_maquina(self, e):
        try:
            busca = self.barra_pesquisa.value.upper()

            query = session.query(Maquina)

            if busca:
                query = query.filter(
                    or_(
                        Maquina.nome_maquina.ilike(f"%{busca}%"),
                        Maquina.setor.ilike(f"%{busca}%")
                    )
                
                )
        
            maquinas = query.all()

            self.tabela.rows = [self.gerar_linha_tabela(maquina) for maquina in maquinas]

            self.texto_aviso.value = f"{len(maquinas)} máquinas encontradas"
            self.texto_aviso.color = ft.Colors.GREEN

            if not maquinas:
                self.texto_aviso.value = "Nenhuma máquina encontrada"
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

            maquinas = session.query(Maquina).filter(Maquina.nome_maquina.like(f"%{busca}%")).all()
            self.tabela.rows.clear()

            for maquina in maquinas:
                self.tabela.rows.append(self.gerar_linha_tabela(maquina))

            if not maquinas:
                self.texto_aviso.value = "Nenhuma máquina encontrada"
                self.texto_aviso.color = ft.Colors.RED
            else:
                self.texto_aviso.value = f"{len(maquinas)} máquinas encontradas"
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

    
