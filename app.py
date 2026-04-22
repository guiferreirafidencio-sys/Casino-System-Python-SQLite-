import flet as ft
import crud
import jogo


def main(page: ft.Page):
    page.title = "Club Cass"

    def fundo():
        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.Colors.BLACK, ft.Colors.BLUE_900]
            )
        )

    # =========================
    # HUB
    # =========================
    def tela_hub(usuario):
        page.clean()

        saldo = ft.Text(
            f"Saldo: R$ {jogo.ver_saldo(usuario):.2f}",
            color="white",
            size=20
        )

        aposta = ft.TextField(label="Valor da aposta", width=200)
        resultado_roleta = ft.Text("", size=30)
        msg = ft.Text("")

        def girar_roleta(e):
            try:
                valor_aposta = float(aposta.value)

                if valor_aposta <= 0:
                    msg.value = "Digite um valor válido"
                    msg.color = ft.Colors.YELLOW
                    page.update()
                    return

                saldo_atual = jogo.ver_saldo(usuario)

                if valor_aposta > saldo_atual:
                    msg.value = "Não possui saldo suficiente"
                    msg.color = ft.Colors.YELLOW
                    page.update()
                    return

            except:
                msg.value = "Digite um número válido"
                msg.color = ft.Colors.RED
                page.update()
                return

            resultado = jogo.girar()
            ganhos = jogo.ganho(resultado, valor_aposta)
            soma = ganhos + valor_aposta

            if soma == 0:
                soma = -valor_aposta

            jogo.mexer_banco(soma, usuario)

            novo_saldo = jogo.ver_saldo(usuario)

            resultado_roleta.value = " | ".join(resultado)

            if soma > 0:
                msg.value = f"Você ganhou R$ {soma:.2f}"
                msg.color = ft.Colors.GREEN
            else:
                msg.value = f"Você perdeu R$ {abs(soma):.2f}"
                msg.color = ft.Colors.RED

            saldo.value = f"Saldo: R$ {novo_saldo:.2f}"

            page.update()

        def voltar(e):
            tela_login()

        page.add(
            ft.Stack([
                fundo(),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column([
                        ft.Text("🎰 Club Cass", size=30, color="white"),
                        aposta,
                        saldo,
                        resultado_roleta,
                        msg,
                        ft.Button("Girar 🎰", on_click=girar_roleta),
                        ft.Button("Voltar", on_click=voltar)
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        tight=True
                    )
                )
            ], expand=True)
        )

    # =========================
    # LOGIN
    # =========================
    def tela_login():
        page.clean()

        user = ft.TextField(label="Usuário", width=250)
        senha = ft.TextField(label="Senha", password=True, width=250)
        resultado = ft.Text("")

        def fazer_login(e):
            verificao = crud.consultar_dados(user.value)

            if verificao and verificao[1] == senha.value:
                tela_hub(user.value)
            else:
                resultado.value = "Usuário ou senha inválidos"
                resultado.color = ft.Colors.RED
                page.update()

        def ir_para_cadastro(e):
            tela_cadastro()

        page.add(
            ft.Stack([
                fundo(),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column([
                        ft.Text("Club Cass", size=30, color="white"),
                        user,
                        senha,
                        ft.Button("Entrar", on_click=fazer_login),
                        ft.Button("Cadastrar", on_click=ir_para_cadastro),
                        resultado
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        tight=True
                    )
                )
            ], expand=True)
        )

    # =========================
    # CADASTRO
    # =========================
    def tela_cadastro():
        page.clean()

        novo_user = ft.TextField(label="Novo usuário", width=250)
        nova_senha = ft.TextField(label="Nova senha", password=True, width=250)
        resposta = ft.Text("")

        def cadastrar(e):
            sucesso = crud.colocar_no_Banco(novo_user.value, nova_senha.value, 18)

            if sucesso:
                resposta.value = "Cadastro realizado!"
                resposta.color = ft.Colors.GREEN
            else:
                resposta.value = "Usuário já existe!"
                resposta.color = ft.Colors.RED

            page.update()

        def voltar(e):
            tela_login()

        page.add(
            ft.Stack([
                fundo(),
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column([
                        ft.Text("Cadastro", size=30, color="white"),
                        novo_user,
                        nova_senha,
                        ft.Button("Cadastrar", on_click=cadastrar),
                        ft.Button("Voltar", on_click=voltar),
                        resposta
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        tight=True
                    )
                )
            ], expand=True)
        )

    tela_login()


ft.run(main)