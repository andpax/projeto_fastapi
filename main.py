# Importa a classe FastAPI, o núcleo do framework.
# Ela é responsável por criar a aplicação web e gerenciar todo o ciclo de vida das requisições HTTP.
from fastapi import FastAPI

# Importa o contexto de criptografia do Passlib.
# O 'CryptContext' é utilizado para gerenciar algoritmos de hash de senhas (como bcrypt),
# facilitando a verificação e atualização de senhas com segurança.
from passlib.context import CryptContext

# Importa a função 'load_dotenv', que carrega variáveis de ambiente
# definidas em um arquivo .env para o ambiente de execução.
# Isso é útil para armazenar credenciais e chaves secretas fora do código-fonte.
from dotenv import load_dotenv

# Importa o módulo 'os' para acessar variáveis de ambiente do sistema.
import os


# Carrega todas as variáveis do arquivo .env.
# Esse passo deve ser feito o mais cedo possível no ciclo de inicialização da aplicação.
load_dotenv()

# Lê a variável de ambiente 'SECRET_KEY' definida no arquivo .env.
# Essa chave é frequentemente usada para assinar tokens JWT ou criptografar dados sensíveis.
SECRET_KEY = os.getenv('SECRET_KEY')


# Instancia a aplicação FastAPI.
# Essa variável 'app' é o ponto central do projeto — todas as rotas, middlewares e eventos são registrados nela.
app = FastAPI(
    title="API de Pedidos e Autenticação",  # (opcional) Define um nome exibido na documentação interativa (Swagger/Redoc)
    version="1.0.0",                        # (opcional) Define a versão da API
    description="Uma API exemplo com rotas de autenticação e gerenciamento de pedidos."  # (opcional)
)


# Cria um contexto de criptografia utilizando o algoritmo bcrypt.
# O parâmetro 'deprecated="auto"' indica que, se um algoritmo for considerado obsoleto,
# o Passlib avisará automaticamente, permitindo atualizações seguras.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Importa os módulos que contêm os "routers" da aplicação.
# Cada módulo define um conjunto de rotas agrupadas por área de responsabilidade:
# - auth_routes: rotas relacionadas à autenticação (login, registro, etc.)
# - order_routes: rotas relacionadas ao gerenciamento de pedidos
from auth_routes import auth_router
from order_routes import order_router


# Registra os routers importados na aplicação principal.
# Isso permite dividir as rotas em módulos separados, tornando o projeto mais organizado e escalável.
# O FastAPI combina automaticamente os prefixos definidos em cada router (ex: "/auth", "/order")
# com o caminho base da aplicação.
app.include_router(auth_router)   # Inclui as rotas de autenticação
app.include_router(order_router)  # Inclui as rotas de pedidos


# ➕ Dica profissional:
# É comum, em projetos maiores, adicionar:
# - Middlewares (para logging, CORS, tratamento de erros globais)
# - Eventos de inicialização e finalização (@app.on_event)
# - Configurações automáticas de banco de dados (via SQLAlchemy ou ORM)
# - Dependências globais (ex: autenticação com JWT)
