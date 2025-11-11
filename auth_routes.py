# Importa o APIRouter do FastAPI, usado para organizar e modularizar as rotas da aplicação.
from fastapi import APIRouter

# Importa o modelo de dados "Usuario" e o objeto "db" (engine do banco) definidos em models.py.
from models import Usuario, db

# Importa o sessionmaker, que serve para criar sessões de comunicação com o banco de dados.
from sqlalchemy.orm import sessionmaker


# Cria um roteador específico para autenticação.
# O prefixo '/auth' será usado em todas as rotas deste módulo.
# A tag 'auth' serve apenas para agrupamento visual na documentação (/docs).
auth_router = APIRouter(prefix='/auth', tags=['auth'])


# ================================================
# 📍 Rota GET - Rota padrão de autenticação
# ================================================
@auth_router.get('/') 
async def home():
    '''
    Essa é a rota padrão de autenticação do nosso sistema.
    Em uma aplicação real, ela poderia verificar se o usuário está autenticado
    (por exemplo, validando um token JWT).
    '''

    # Retorna uma mensagem simples em formato JSON.
    # Essa rota serve apenas como ponto de partida para a área de autenticação.
    return {
        'menssagem': 'Você acessou a rota padrão de autenticação.',
        'autenticado': False
    }


# ================================================
# 🧑‍💻 Rota POST - Criação de nova conta de usuário
# ================================================
@auth_router.post('/criar_conta')
async def criar_conta(email: str, senha: str, nome: str):
    '''
    Cria um novo usuário no banco de dados.

    Parâmetros recebidos via corpo da requisição:
    - email: endereço de e-mail do usuário.
    - senha: senha de acesso (idealmente deve ser criptografada).
    - nome: nome completo do usuário.
    '''

    # Cria uma fábrica de sessões (Session), vinculada ao banco configurado (db).
    Session = sessionmaker(bind=db)

    # Cria uma nova sessão para interagir com o banco.
    # As sessões são responsáveis por executar consultas, inserções e commits.
    session = Session()

    # Verifica se já existe um usuário com o mesmo e-mail cadastrado.
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    
    # Caso já exista, retorna uma mensagem de erro.
    if usuario:
        return {'mensagem': 'Já existe um usuário com esse e-mail!'}

    # Caso não exista, cria um novo registro de usuário.
    else:
        # Cria um novo objeto da classe Usuario.
        # ⚠️ OBS: o modelo atual exige 5 parâmetros no construtor (nome, email, senha, ativo, admin),
        # mas aqui foram passados apenas 3. É preciso ajustar o modelo ou incluir os valores faltantes.
        novo_usuario = Usuario(nome, email, senha, ativo=True, admin=False)

        # Adiciona o novo usuário à sessão.
        session.add(novo_usuario)

        # Grava as alterações no banco (commit).
        session.commit()

        # Fecha a sessão (boa prática).
        session.close()

        # Retorna mensagem de sucesso.
        return {'mensagem': 'Usuário cadastrado com sucesso!'}
