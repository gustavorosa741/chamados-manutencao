import flet as ft
from DB.database import session

class MenuPrincipal:
    def __init__(self, page: ft.Page):
        page.title = "Menu Principal"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.START

        self.page = page
        self.content_area = ft.Column(expand=True)

        def fechar_app(e):
            page.clean()
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.add(ft.Text("Aplicação fechada."))
            session.close()

        def menu_clicked(e):
            self.content_area.controls.clear()
            self.content_area.controls.append(ft.Text(f"Clicou em: {e.control.text}"))
            page.update()

        def abrir_cadastro_funcionario(e):
            from Models.cadastro_funcionario import CadastroUsuario
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroUsuario().get_container())
            page.update()

        def abrir_lista_funcionario(e):
            from Models.cadastro_funcionario import ListarUsuario
            self.content_area.controls.clear()
            self.content_area.controls.append(ListarUsuario(page).get_container())
            page.update()

        def abrir_cadastro_maquina(e):
            from Models.cadastro_maquina import CadastroMaquina
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroMaquina().get_container())
            page.update()
        
        def abrir_lista_maquina(e):
            from Models.cadastro_maquina import ListarMaquina
            self.content_area.controls.clear()
            self.content_area.controls.append(ListarMaquina(page).get_container())
            page.update()

        def abrir_cadastro_chamado(e):
            from Models.cadastro_chamado import CadastroChamado
            self.content_area.controls.clear()
            self.content_area.controls.append(CadastroChamado().get_container())
            page.update()





        menu_superior = ft.Container(
            content=ft.Row(
                controls=[
                    ft.PopupMenuButton(
                        content=ft.Text("Cadastrar", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Novo Chamado", on_click=abrir_cadastro_chamado),
                            ft.PopupMenuItem(text="Novo Usuario", on_click=abrir_cadastro_funcionario),
                            ft.PopupMenuItem(text="Nova Máquina", on_click=abrir_cadastro_maquina),
                            
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Consultar", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Lista de Chamados", on_click=menu_clicked),
                            ft.PopupMenuItem(text="Lista de Usuarios", on_click=abrir_lista_funcionario),
                            ft.PopupMenuItem(text="Lista de Máquinas", on_click=abrir_lista_maquina),
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Relatórios", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Relatorios", on_click=menu_clicked),
                        ]
                    ),
                    ft.PopupMenuButton(
                        content=ft.Text("Sair", weight=ft.FontWeight.BOLD),
                        items=[
                            ft.PopupMenuItem(text="Fechar Aplicação", on_click=lambda e: fechar_app(e)),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            ),
            padding=10,
            bgcolor=ft.Colors.BLUE_700,
            border_radius=5
        )

        page.add(
            ft.Column(
                [
                    menu_superior,
                    ft.Divider(thickness=2),
                    self.content_area
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True
            )
        )

        self.content_area.controls.append(ft.Text("Bem-vindo ao sistema de chamados!", size=24))
        page.update()