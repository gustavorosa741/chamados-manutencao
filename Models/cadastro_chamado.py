import flet as ft
from sqlalchemy import or_
from DB.database import session
from Tables.maquina import Maquina
from Tables.chamado import Chamado

def formatacao(e):
    #remove espaços e converte para maiúsculas
    e.control.value = e.control.value.upper()
    e.control.update()


class CadastroChamado:
    def __init__(self):
        self.nome = ft.Dropdown(
            label="Máquina",
            hint_text="Selecione a máquina",
            width=350,
            border_radius=10,
            prefix_icon=ft.Icons.HARDWARE,
            on_change=formatacao,
        )

        self.data_inicio = ft.TextField(
            label="Data de Início",
            hint_text="Digite a data de início",
            width=350,
            border_radius=10,
            prefix_icon=ft.Icons.DATE_RANGE,
            on_change=formatacao,
        )

        self.problema = ft.TextField(
            label="Problema",
            hint_text="Digite o problema",
            width=350,
            border_radius=10,
            prefix_icon=ft.Icons.BUG_REPORT,
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
                    ft.Text("Cadastro de Chamado", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    self.nome,
                    self.data_inicio,
                    self.problema,
                    self.texto_aviso,
                    self.botao_cadastrar
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ) 
    

    def cadastrar_maquina(self, e):
        nome = self.nome
        data_inicio = self.data_inicio
        problema = self.problema

        try:

            if not all ([nome, data_inicio, problema]):
                self.texto_aviso.value = "Preencha todos os campos!"
                self.texto_aviso.color = ft.Colors.RED
                e.page.update()
                
            else:
                novo_chamado = Chamado(nome_maquina=nome.value, data_abertura=data_inicio.value, problema=problema.value)
                session.add(novo_chamado)
                session.commit()

                self.texto_aviso.value = "Chamado cadastrado com sucesso"
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