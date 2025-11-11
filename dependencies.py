# Importa o objeto 'db' (conexão com o banco de dados) definido no módulo models.
from models import db

# Importa o 'sessionmaker' do SQLAlchemy, responsável por criar fábricas de sessão.
# Cada sessão representa uma conexão temporária com o banco para executar operações (SELECT, INSERT, UPDATE, DELETE).
from sqlalchemy.orm import sessionmaker


# Cria uma fábrica de sessões chamada 'SessionLocal', associada ao banco de dados 'db'.
# Isso permite criar novas sessões sem precisar configurar a conexão toda vez.
SessionLocal = sessionmaker(bind=db)


def pegar_sessao():
    """
    Função usada como dependência no FastAPI para fornecer uma sessão de banco de dados por requisição.

    Essa função é do tipo generator (usa 'yield') e segue o padrão recomendado pelo FastAPI:
    - Cria a sessão no início.
    - Entrega (yield) a sessão para a rota que a solicitou.
    - Fecha a sessão automaticamente no final da requisição (no bloco 'finally').
    """

    # Cria uma nova sessão a partir da fábrica definida acima.
    session = SessionLocal()
    
    try:
        # Entrega a sessão para o endpoint que solicitou a dependência.
        # Durante o uso, o FastAPI injeta essa sessão na rota.
        yield session
    finally:
        # Esse bloco é executado após o término da requisição, com ou sem erro.
        # Fecha a sessão para liberar recursos e evitar conexões abertas.
        session.close()
