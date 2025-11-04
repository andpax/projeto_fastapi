# Importa a classe APIRouter do FastAPI.
# Ela é usada para criar e organizar grupos de rotas de forma independente.
# Isso facilita a manutenção e deixa o projeto mais modular.
from fastapi import APIRouter


# Cria um roteador (router) específico para as rotas de autenticação.
# O prefixo '/auth' indica que todas as rotas deste arquivo começarão com esse caminho.
# As "tags" são usadas apenas para fins de documentação, facilitando a visualização no Swagger UI (/docs).
auth_router = APIRouter(prefix='/auth', tags=['auth'])


# Define uma rota do tipo GET dentro do roteador de autenticação.
# O decorator '@auth_router.get('/')' conecta a função abaixo à rota '/auth/'.
# Assim, quando o usuário acessa '/auth/', a função 'autenticar()' é executada.
@auth_router.get('/')
async def autenticar():
    '''
    Essa é a rota padrão de autenticação do nosso sistema.
    Em uma aplicação real, ela poderia ser usada para verificar se o usuário está logado
    ou redirecionar para uma rota de login.
    '''

    # Retorna uma resposta JSON.
    # Neste exemplo, apenas informa que o acesso à rota de autenticação ocorreu com sucesso,
    # mas o campo 'autenticado' ainda é False (ou seja, não autenticado).
    return {
        'menssagem': 'Você acessou a rota padrão de autenticação.',
        'autenticado': False
    }
