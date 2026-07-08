import json
import os

# Pasta e arquivos onde os dados ficam persistidos
PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ARQ_USUARIOS = os.path.join(PASTA_DADOS, "usuarios.json")
ARQ_SERVICOS = os.path.join(PASTA_DADOS, "servicos.json")
ARQ_AGENDAMENTOS = os.path.join(PASTA_DADOS, "agendamentos.json")


def _garantir_pasta():
    '''Cria a pasta data/ caso ela ainda não exista'''
    os.makedirs(PASTA_DADOS, exist_ok=True)


def _carregar(caminho, padrao):
    '''Função genérica de leitura: se o arquivo não existir ou estiver
    corrompido, cria um novo com o valor padrão (evita o programa quebrar
    na primeira execução, como pede o documento)'''
    _garantir_pasta()

    if not os.path.exists(caminho):
        _salvar(caminho, padrao)
        return padrao

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        # Arquivo vazio/corrompido: recria com o padrão em vez de travar
        _salvar(caminho, padrao)
        return padrao


def _salvar(caminho, dados):
    '''Função genérica de escrita, usada por todas as funções salvar_*'''
    _garantir_pasta()
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


# ---------------- Usuários ----------------
# Estrutura sugerida no documento:
# { "id_do_usuario": {"nome", "email", "senha", "telefone", "tipo": "cliente"|"admin"} }

def carregar_usuarios():
    return _carregar(ARQ_USUARIOS, {})


def salvar_usuarios(usuarios):
    _salvar(ARQ_USUARIOS, usuarios)


# ---------------- Serviços ----------------

def carregar_servicos():
    return _carregar(ARQ_SERVICOS, {})


def salvar_servicos(servicos):
    _salvar(ARQ_SERVICOS, servicos)


# ---------------- Agendamentos ----------------

def carregar_agendamentos():
    return _carregar(ARQ_AGENDAMENTOS, {})


def salvar_agendamentos(agendamentos):
    _salvar(ARQ_AGENDAMENTOS, agendamentos)
