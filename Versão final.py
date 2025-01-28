import flet as ft

def main(page: ft.Page):
    # Configurar estilo da página
    page.title = "Chat do Marco"
    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.scroll = "auto"  # Permitir rolagem se necessário

    # Título estilizado
    titulo = ft.Text(
        "Chat do Marco",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_500,
        text_align=ft.TextAlign.CENTER,
    )

    # Área do chat
    chat = ft.Column(spacing=10, expand=True)  # Expand para ocupar o espaço disponível
    chat = ft.Column(scroll="auto", auto_scroll=True, expand=True)
    # Campo de nome do usuário
    nome_usuario = ft.TextField(
        label="Escreva seu nome",
        border_color=ft.colors.GREY_400,
        filled=True,
        fill_color=ft.colors.BLUE_GREY_50,
        border_radius=8,
    )

    # Função para enviar mensagens via túnel
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(
                ft.Container(
                    content=ft.Text(f"{usuario_mensagem}: {texto_mensagem}", size=14),
                    bgcolor=ft.colors.BLUE_50 if usuario_mensagem != "Você" else ft.colors.GREEN_50,
                    border_radius=10,
                    padding=10,
                    margin=5,
                )
            )
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(
                ft.Text(
                    f"{usuario_mensagem} entrou no chat",
                    size=12,
                    italic=True,
                    color=ft.colors.ORANGE_500,
                )
            )
        page.update()

    # Inscrever função no pubsub
    page.pubsub.subscribe(enviar_mensagem_tunel)

    # Campo de mensagem
    campo_mensagem = ft.TextField(
        label="Digite uma mensagem",
        border_color=ft.colors.GREY_400,
        filled=True,
        fill_color=ft.colors.BLUE_GREY_50,
        border_radius=8,
        on_submit=lambda e: enviar_mensagem(e),
    )

    # Botão de enviar mensagem
    botao_enviar_mensagem = ft.ElevatedButton(
        "Enviar",
        on_click=lambda e: enviar_mensagem(e),
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
    )

    # Função para enviar mensagem
    def enviar_mensagem(evento):
        if nome_usuario.value.strip() and campo_mensagem.value.strip():
            page.pubsub.send_all(
                {"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"}
            )
            campo_mensagem.value = ""
            page.update()

    # Função para lidar com entrada no chat
    def entrar_popup(evento):
        if nome_usuario.value.strip():
            page.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
            page.add(chat)
            popup.open = False
            page.remove(botao_iniciar)
            page.remove(titulo)
            page.add(ft.Row([campo_mensagem, botao_enviar_mensagem], spacing=10))
            page.update()

    # Popup de entrada
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text(
            "Bem-vindo ao Chat do Marco",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.TEAL_700,
        ),
        content=nome_usuario,
        actions=[
            ft.ElevatedButton(
                "Entrar",
                on_click=entrar_popup,
                bgcolor=ft.colors.GREEN_500,
                color=ft.colors.WHITE,
            )
        ],
    )

    # Função para exibir o popup
    def entrar_chat(evento):
        page.dialog = popup
        popup.open = True
        page.update()

    # Botão para iniciar o chat
    botao_iniciar = ft.ElevatedButton(
        "Iniciar Chat",
        on_click=entrar_chat,
        bgcolor=ft.colors.ORANGE_500,
        color=ft.colors.WHITE,
    )

    # Adicionar componentes à página
    page.add(titulo, botao_iniciar)

# Executar o app
ft.app(target=main)
