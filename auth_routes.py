# Importa o APIRouter, que permite organizar as rotas da aplicação em módulos separados.
# Também importa Depends (para injeção de dependências) e HTTPException (para erros HTTP personalizados).
from fastapi import APIRouter, Depends, HTTPException

# Importa o modelo de banco de dados 'Usuario' definido no módulo 'models'.
from models import Usuario

# Importa a função responsável por gerenciar a sessão com o banco de dados.
from dependencies import pegar_sessao

# Importa o contexto de criptografia bcrypt definido no arquivo principal (main.py).
from main import bcrypt_context

# Importa o schema de validação 'UsuarioSchema', que define como os dados do usuário devem ser recebidos e validados.
# Importa o schema de validação 'LoginSchema', que define como os dados do login devem ser recebidos e validados.
from schemas import UsuarioSchema, LoginSchema

# Importa o tipo 'Session' do SQLAlchemy, usado para digitar a dependência do banco.
from sqlalchemy.orm import Session


# Cria um roteador específico para autenticação.
# Todas as rotas desse módulo terão o prefixo '/auth' e serão agrupadas sob a tag 'auth' na documentação do FastAPI.
auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criar_token(id_usuario):
    token = f'fue8350je373$.{id_usuario}'
    return token


@auth_router.get('/')
async def home():
    '''
    Rota padrão da autenticação.

    Objetivo:
    - Retornar uma mensagem informativa sobre o módulo de autenticação.
    - Poderia, em um cenário real, validar um token JWT ou cookie de sessão para verificar se o usuário está logado.
    '''

    return {
        'menssagem': 'Você acessou a rota padrão de autenticação.',
        'autenticado': False
    }


@auth_router.post('/criar_conta')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    '''
    Rota responsável por criar um novo usuário no banco de dados.

    Parâmetros:
    - usuario_schema: objeto validado via Pydantic (contém nome, e-mail, senha, ativo e admin).
    - session: instância de sessão do SQLAlchemy, gerenciada automaticamente pela dependência 'pegar_sessao'.

    Processo:
    1. Verifica se o e-mail informado já existe no banco.
    2. Se existir, lança uma exceção HTTP 400.
    3. Se não existir, criptografa a senha com bcrypt.
    4. Cria um novo registro de usuário no banco.
    5. Retorna mensagem de sucesso.

    Observação:
    - Em um cenário real, seria necessário validar:
        • formato do e-mail;
        • força e comprimento da senha;
        • duplicidade de e-mails;
        • política de criação de usuários (ex: apenas admin pode criar novos usuários).
    '''

    # Verifica se já existe um usuário com o e-mail informado.
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    
    # Se o usuário já existe, retorna erro HTTP 400 (Bad Request).
    if usuario:
        raise HTTPException(status_code=400, detail='E-mail do usuário já cadastrado.') 

    else:
        # Garante que a senha tenha um tamanho máximo de 72 bytes antes da criptografia.
        # Isso evita erros no bcrypt, que tem esse limite.
        senha_ajustada = usuario_schema.senha.encode("utf-8")[:72].decode("utf-8", errors="ignore")

        # Criptografa a senha usando o contexto bcrypt definido no main.py.
        senha_criptografada = bcrypt_context.hash(senha_ajustada)

        # Cria uma nova instância do modelo 'Usuario' para ser persistida no banco.
        novo_usuario = Usuario(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_criptografada,
            ativo=usuario_schema.ativo,
            admin=usuario_schema.admin
        )

        # Adiciona o novo usuário à sessão do banco.
        session.add(novo_usuario)

        # Confirma a transação, salvando as alterações no banco de dados.
        session.commit()

        # Retorna uma mensagem de sucesso com o e-mail do usuário criado.
        return {'mensagem': f'Usuário cadastrado com sucesso: {usuario_schema.email}'}

    
# ===============================================
# 🔐 ROTA POST — Login de usuário
# ===============================================
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    '''
    Realiza o login de um usuário autenticando suas credenciais.

    Parâmetros (via corpo da requisição):
    - email: e-mail cadastrado do usuário.
    - senha: senha em texto puro (que será comparada com a senha criptografada do banco).

    O retorno é um token de acesso (JWT, por exemplo), que será usado para autenticação nas demais rotas.
    '''

    # Busca o usuário no banco de dados com base no e-mail informado.
    usuario = session.query(Usuario).filter(UsuarioSchema.email == login_schema).first()

    # Se o usuário não existir, lança um erro 400 (Bad Request).
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado')

    # Verifica se a senha informada confere com a senha armazenada (criptografada).
    senha_valida = bcrypt_context.verify(login_schema.senha, usuario.senha)

    # Caso a senha esteja incorreta, retorna erro 401 (não autorizado).
    if not senha_valida:
        raise HTTPException(status_code=401, detail='Senha incorreta')

    # Caso o login seja bem-sucedido, gera um token de acesso.
    # OBS: A função "criar_token" deve ser implementada em um módulo de utilitários
    # (ex: utils/security.py) e retornar um JWT contendo o ID do usuário.
    access_token = criar_token(usuario.id)

    # Retorna o token e o tipo do token (padrão Bearer).
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }
