from src import dados
from src import servicos
from datetime import datetime

def carregar_agendamentos():
    '''Carrega os agendamentos a partir do arquivo JSON'''
    return dados.carregar_agendamentos()


def _proximo_id(agendamentos):
    '''Gera o próximo id sequencial, com base no maior id numérico
    já existente nos agendamentos. Ex.: se existem "1" e "2", o próximo
    será "3".'''
    if not agendamentos:
        return "1"
    return str(max(int(id_agendamento) for id_agendamento in agendamentos.keys()) + 1)


def listar_agendamentos(agendamentos):
    '''Mostra todos os agendamentos feitos até o momento. Retorna True se havia
    algo pra mostrar, False se a agenda estiver vazia.'''
    if not agendamentos:
        print("| Nenhum agendamento no momento.")
        return False

    print("\n| Agendamentos:")
    # Ordena pelo id numérico para a lista sempre aparecer em ordem (1, 2, 3...)
    for id_agendamento in sorted(agendamentos.keys(), key=int):
        agendamento = agendamentos[id_agendamento]
        print(
            f"| {id_agendamento} - {agendamento['nome_cliente']} | "
            f"{agendamento['nome_servico']} | {agendamento['data']} "
            f"{agendamento['hora']} | status: {agendamento['status']}"
        )
    return True


def listar_agendamentos_do_dia(agendamentos, data=None):
    '''Mostra os agendamentos de uma data específica, ordenados por horário.
    Pensada para o menu do admin ("ver agendamentos do dia"). Se `data` não
    for passada, pede ao usuário. Retorna True se havia algo pra mostrar
    naquele dia, False se a data for inválida ou não houver nada agendado.'''

    if data is None:
        data = input("| Ver agendamentos de qual data (ex: 25/03/2026): ").strip()

    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        print("| Data em formato inválido.")
        return False

    # Filtra só os agendamentos daquele dia
    agendamentos_do_dia = {
        id_ag: ag for id_ag, ag in agendamentos.items() if ag["data"] == data
    }

    if not agendamentos_do_dia:
        print(f"| Nenhum agendamento para o dia {data}.")
        return False

    # Ordena por horário (string "HH:MM" ordena certo como texto,
    # já que o formato é sempre de dois dígitos)
    print(f"\n| Agendamentos do dia {data}:")
    for id_ag in sorted(agendamentos_do_dia, key=lambda i: agendamentos_do_dia[i]["hora"]):
        ag = agendamentos_do_dia[id_ag]
        print(
            f"| {ag['hora']} - {ag['nome_cliente']} | "
            f"{ag['nome_servico']} | status: {ag['status']}"
        )
    return True


def adicionar_agendamento(agendamentos, catalogo_servicos, id_cliente, nome_cliente):
    '''Cadastra um novo horário na agenda, checando conflito de horário
    antes de salvar.'''
    while True:
        print("| Fazer Agendamento")

        # Mostra a lista de serviços oferecidos pelo salão para o cliente escolher
        if not servicos.listar_servicos(catalogo_servicos):
            return

        id_servico = input("| Número do serviço: ").strip()
        if id_servico not in catalogo_servicos:
            print("| Serviço não encontrado.")
            return

        # Seleção da data/horário de atendimento
        data = input("| Data (ex: 25/03/2026): ").strip()
        horario = input("| Horário (ex: 16:30): ").strip()

        try:
            datetime.strptime(data, "%d/%m/%Y")
            datetime.strptime(horario, "%H:%M")
        except ValueError:
            print("| Data ou horário em formato inválido.")
            continue

        # Verifica se já existe outro agendamento ATIVO no mesmo data+hora
        horario_ocupado = False
        for id_ag, ag in agendamentos.items():
            if ag["data"] == data and ag["hora"] == horario and ag["status"] == "agendado":
                horario_ocupado = True
                break

        if horario_ocupado:
            print("| Esse horário já está ocupado. Escolha outro.")
            continue

        novo_id_agendamento = _proximo_id(agendamentos)
        agendamentos[novo_id_agendamento] = {
            "id": novo_id_agendamento,
            "id_cliente": id_cliente,
            "nome_cliente": nome_cliente,
            "id_servico": id_servico,
            "nome_servico": catalogo_servicos[id_servico]["nome"],
            "data": data,
            "hora": horario,
            "status": "agendado",
        }

        dados.salvar_agendamentos(agendamentos)
        print("| Agendamento realizado com sucesso.")
        break


def cancelar_agendamento(agendamentos, id_cliente):
    '''Cancela um agendamento do cliente logado. Em vez de apagar o registro,
    apenas muda o status para "cancelado", preservando o histórico (como
    o documento sugere com os três status possíveis).'''

    # Filtra só os agendamentos DESSE cliente que ainda estão ativos
    agendamentos_cliente = {}
    for id_ag, ag in agendamentos.items():
        if ag["id_cliente"] == id_cliente and ag["status"] == "agendado":
            agendamentos_cliente[id_ag] = ag

    if not agendamentos_cliente:
        print("| Você não possui agendamentos ativos para cancelar.")
        return

    print("\n| Seus agendamentos ativos:")
    for id_ag, ag in agendamentos_cliente.items():
        print(f"| {id_ag} - {ag['nome_servico']}: {ag['data']} {ag['hora']}")

    id_cancelado = input("| Qual agendamento deseja cancelar (informe o número): ").strip()

    # Verifica dentro de agendamentos_cliente, não de agendamentos inteiro —
    # impede o cliente de cancelar um agendamento de outra pessoa
    if id_cancelado not in agendamentos_cliente:
        print("| Agendamento não encontrado entre os seus.")
        return

    confirmacao = input("| Confirma o cancelamento? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("| Operação cancelada.")
        return

    agendamentos[id_cancelado]["status"] = "cancelado"
    dados.salvar_agendamentos(agendamentos)
    print("| Agendamento cancelado com sucesso.")
