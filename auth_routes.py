# Importa o APIRouter (para criar grupos de rotas) e o Depends (para injeção de dependências).
from fastapi import APIRouter, Depends

# Importa o modelo de usuário (classe Usuario) que representa a tabela no banco de dados.
from models import Usuario

# Importa a função 'pegar_sessao', que será usada como dependência para abrir e fechar a sessão do banco.
from dependencies import pegar_sessao


# Cria um roteador específico para autenticação.
# - prefix: todas as rotas desse módulo terão o caminho base "/auth".
# - tags: agrupa as rotas no Swagger UI (/docs) para melhor visualização.
auth_router = APIRouter(prefix='/auth', tags=['auth'])


# ===============================================
# 📍 ROTA GET — Rota padrão de autenticação
# ===============================================
@auth_router.get('/')
async def home():
    '''
    Essa é a rota padrão de autenticação do sistema.
    Em um sistema real, essa rota poderia verificar se o usuário está autenticado
    (por exemplo, validando um token JWT).
    '''

    # Retorna uma resposta simples em formato JSON.
    # Aqui é apenas uma rota ilustrativa.
    return {
        'menssagem': 'Você acessou a rota padrão de autenticação.',
        'autenticado': False
    }


# ===============================================
# 🧑‍💻 ROTA POST — Criação de nova conta de usuário
# ===============================================
@auth_router.post('/criar_conta')
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    '''
    Cria um novo usuário no banco de dados.

    Parâmetros recebidos via corpo da requisição:
    - email: endereço de e-mail do usuário.
    - senha: senha de acesso (idealmente deve ser criptografada).
    - nome: nome completo do usuário.

    A sessão de banco de dados é obtida automaticamente através da dependência 'pegar_sessao',
    que garante a abertura e o fechamento da conexão de forma segura.
    '''

    # Verifica se já existe um usuário com o e-mail informado.
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    
    # Caso o e-mail já esteja cadastrado, retorna uma mensagem de erro.
    if usuario:
        return {'mensagem': 'Já existe um usuário com esse e-mail!'}

    # Caso contrário, cria um novo registro no banco.
    else:
        # Instancia um novo usuário com os dados fornecidos.
        # Os campos "ativo" e "admin" são definidos manualmente.
        novo_usuario = Usuario(nome, email, senha, ativo=True, admin=False)

        # Adiciona o novo usuário à sessão (ainda não grava no banco).
        session.add(novo_usuario)

        # Grava as alterações de forma permanente no banco.
        session.commit()

        # Retorna uma mensagem de sucesso.
        return {'mensagem': 'Usuário cadastrado com sucesso!'}
