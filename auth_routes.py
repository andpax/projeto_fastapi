# ============================================================
# 📦 Importações principais
# ============================================================

# Importa o APIRouter (para criar grupos de rotas) e o Depends (para injeção de dependências).
# O Depends é usado para "injetar" automaticamente objetos ou funções
# em endpoints, como sessões de banco de dados.
from fastapi import APIRouter, Depends

# Importa o modelo de usuário (classe Usuario) que representa a tabela no banco de dados.
# Essa classe foi criada com SQLAlchemy.
from models import Usuario

# Importa a função 'pegar_sessao', responsável por criar e gerenciar a sessão do banco.
# Essa função utiliza um generator com "yield", garantindo que a sessão
# seja aberta e fechada corretamente em cada requisição.
from dependencies import pegar_sessao

# Importa o contexto do bcrypt criado no main.py.
# Ele será usado para criptografar senhas antes de salvar no banco.
from main import bcrypt_context


# ============================================================
# ⚙️ Configuração do roteador
# ============================================================

# Cria um roteador específico para autenticação.
# - prefix: todas as rotas desse módulo terão o caminho base "/auth".
# - tags: agrupa as rotas no Swagger UI (/docs) para melhor organização visual.
auth_router = APIRouter(prefix='/auth', tags=['auth'])


# ============================================================
# 📍 ROTA GET — Rota padrão de autenticação
# ============================================================

@auth_router.get('/')
async def home():
    '''
    Essa é a rota padrão de autenticação do sistema.
    Em um sistema real, essa rota poderia verificar se o usuário está autenticado
    (por exemplo, validando um token JWT).
    '''

    # Retorna uma resposta simples em formato JSON.
    # Aqui é apenas uma rota ilustrativa, sem validação real de login.
    return {
        'menssagem': 'Você acessou a rota padrão de autenticação.',
        'autenticado': False
    }


# ============================================================
# 🧑‍💻 ROTA POST — Criação de nova conta de usuário
# ============================================================

@auth_router.post('/criar_conta')
async def criar_conta(
    email: str,
    senha: str,
    nome: str,
    session = Depends(pegar_sessao)
):
    '''
    Cria um novo usuário no banco de dados.

    Parâmetros recebidos via corpo da requisição:
    - email: endereço de e-mail do usuário.
    - senha: senha de acesso (idealmente deve ser criptografada).
    - nome: nome completo do usuário.

    A sessão de banco de dados é obtida automaticamente através da dependência 'pegar_sessao',
    que garante a abertura e o fechamento da conexão de forma segura.

    Obs: Em um cenário real, essa rota deve validar:
      - formato do e-mail;
      - tamanho mínimo da senha;
      - duplicidade de registros.
    '''

    # 🔎 Verifica se já existe um usuário com o e-mail informado.
    # O método "filter(...).first()" retorna o primeiro resultado encontrado (ou None se não houver).
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    
    # 🚫 Caso o e-mail já esteja cadastrado, retorna uma mensagem de erro.
    if usuario:
        return {'mensagem': 'Já existe um usuário com esse e-mail!'}

    # ✅ Caso contrário, cria um novo registro no banco.
    else:
        # O bcrypt aceita senhas com até 72 caracteres.
        # Aqui fazemos um ajuste para evitar erros em senhas longas.
        senha_ajustada = senha.encode("utf-8")[:72].decode("utf-8", errors="ignore")

        # Criptografa a senha antes de salvar no banco.
        # Isso é essencial para a segurança, pois evita armazenar senhas em texto puro.
        senha_criptografada = bcrypt_context.hash(senha_ajustada)

        # Instancia um novo usuário com os dados fornecidos.
        # Os campos "ativo" e "admin" são definidos manualmente.
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_criptografada,
            ativo=True,
            admin=False
        )

        # Adiciona o novo usuário à sessão (ainda não grava no banco).
        session.add(novo_usuario)

        # Grava as alterações de forma permanente no banco de dados.
        session.commit()

        # Boa prática: você pode usar "session.refresh(novo_usuario)"
        # para atualizar o objeto com dados como o "id" gerado automaticamente.

        # Retorna uma mensagem de sucesso para o cliente.
        return {'mensagem': 'Usuário cadastrado com sucesso!'}
