from src import dados


def carregar_catalogo():
    '''Carrega o catálogo de serviços a partir do arquivo JSON'''
    return dados.carregar_servicos()


def _proximo_id(servicos):
    '''Gera o próximo id sequencial, com base no maior id numérico
    já existente no catálogo. Ex.: se existem "1" e "2",o próximo
    será "3".'''
    if not servicos:
        return "1"
    return str(max(int(id_servico) for id_servico in servicos.keys()) + 1)


def listar_servicos(servicos):
    '''Mostra o catálogo formatado. Retorna True se havia algo
    pra mostrar, False se o catálogo está vazio.'''
    if not servicos:
        print("| Nenhum serviço cadastrado no momento.")
        return False

    print("\n| Catálogo de serviços:")
    # Ordena pelo id numérico para a lista sempre aparecer em ordem (1, 2, 3...)
    for id_servico in sorted(servicos.keys(), key=int):
        servico = servicos[id_servico]
        print(
            f"| {id_servico} - {servico['nome']} "
            f"(R$ {servico['preco']:.2f}, {servico['duracao']} min)"
        )
    return True


def adicionar_servico(servicos):
    '''Cadastra um novo serviço no catálogo.'''
    print("| Cadastro de novo serviço")

    nome = input("| Nome: ").strip()
    descricao = input("| Descrição: ").strip()

    if not nome:
        print("| O nome do serviço não pode ficar em branco.")
        return

    try:
        preco = float(input("| Preço (ex: 80.00): "))
        duracao = int(input("| Duração em minutos (ex: 60): "))
    except ValueError:
        print("| Preço ou duração inválidos. Cadastro cancelado.")
        return

    novo_id = _proximo_id(servicos)
    servicos[novo_id] = {
        "id": novo_id,
        "nome": nome,
        "preco": preco,
        "duracao": duracao,
        "descricao": descricao,
    }

    dados.salvar_servicos(servicos)
    print(f"| Serviço '{nome}' cadastrado com sucesso (id {novo_id}).")


def editar_servico(servicos):
    '''Edita um serviço existente.
    Deixa o usuário apertar Enter em branco para manter o valor atual.'''
    if not listar_servicos(servicos):
        return

    id_escolhido = input("| Digite o número do serviço que deseja editar: ").strip()

    if id_escolhido not in servicos:
        print("| Serviço não encontrado.")
        return

    servico = servicos[id_escolhido]
    print(f"| Editando '{servico['nome']}'. Deixe em branco para manter o valor atual.")

    novo_nome = input(f"| Nome [{servico['nome']}]: ").strip()
    nova_descricao = input(f"| Descrição [{servico['descricao']}]: ").strip()
    novo_preco = input(f"| Preço [{servico['preco']:.2f}]: ").strip()
    nova_duracao = input(f"| Duração em minutos [{servico['duracao']}]: ").strip()

    if novo_nome:
        servico["nome"] = novo_nome
    if nova_descricao:
        servico["descricao"] = nova_descricao
    if novo_preco:
        try:
            servico["preco"] = float(novo_preco)
        except ValueError:
            print("| Preço inválido, mantido o valor anterior.")
    if nova_duracao:
        try:
            servico["duracao"] = int(nova_duracao)
        except ValueError:
            print("| Duração inválida, mantido o valor anterior.")

    dados.salvar_servicos(servicos)
    print("| Serviço atualizado com sucesso.")


def remover_servico(servicos):
    '''Remove um serviço do catálogo. '''
    if not listar_servicos(servicos):
        return

    id_escolhido = input("| Digite o número do serviço que deseja remover: ").strip()

    if id_escolhido not in servicos:
        print("| Serviço não encontrado.")
        return

    nome_removido = servicos[id_escolhido]["nome"]
    confirmacao = input(f"| Confirma remover '{nome_removido}'? (s/n): ").strip().lower()

    if confirmacao == "s":
        del servicos[id_escolhido]
        dados.salvar_servicos(servicos)
        print("| Serviço removido com sucesso.")
    else:
        print("| Remoção cancelada.")
