import curses

from src import dados
from src.login import entrada_do_sistema, login
from src.cadastro import cadastro


def main():
    '''Ponto de entrada do sistema. Carrega os dados, mostra o menu inicial
    (Login / Criar Conta) e direciona para o módulo correspondente. O login
    e o cadastro, por sua vez, já cuidam de redirecionar para o menu do
    cliente ou do administrador (ver login.py e cadastro.py).'''

    # Garante que sempre exista pelo menos um administrador, mesmo na
    # primeira execução do sistema ou se usuarios.json for apagado
    dados.garantir_admin_padrao()

    usuarios = dados.carregar_usuarios()

    while True:
        # curses.wrapper cuida de inicializar e restaurar o terminal
        # corretamente, mesmo se ocorrer algum erro dentro da função
        escolha = curses.wrapper(entrada_do_sistema)

        if escolha == "login":
            login(usuarios)
        elif escolha == "cadastro":
            cadastro(usuarios)

        continuar = input("\n| Voltar ao menu inicial? (s/n): ").strip().lower()
        if continuar != "s":
            print("| Até logo!")
            break


if __name__ == "__main__":
    main()
