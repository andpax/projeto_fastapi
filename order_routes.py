# Importa a classe APIRouter do FastAPI.
# Ela é usada para criar grupos de rotas independentes, permitindo organizar
# o código de forma modular (por exemplo, rotas de autenticação, pedidos, produtos, etc.).
from fastapi import APIRouter


# Cria um "roteador" (router) específico para as rotas de pedidos.
# O parâmetro 'prefix' define o caminho base para todas as rotas deste módulo.
# O parâmetro 'tags' é opcional e serve apenas para agrupar rotas na documentação automática do FastAPI (Swagger UI).
order_router = APIRouter(prefix='/orders', tags=['orders'])


# Define uma rota do tipo GET dentro do roteador de pedidos.
# O símbolo '@' indica um "decorator" que conecta a função abaixo à rota '/orders/'.
@order_router.get('/')
async def pedidos():
    '''
    Essa é a rota padrão de pedidos do nosso sistema.
    Todas as rotas de pedidos precisam de autenticação.
    (Observação: o controle de autenticação pode ser feito com dependências, middlewares ou tokens JWT.)
    '''

    # Retorna uma resposta JSON com uma mensagem simples.
    # Aqui estamos apenas confirmando o acesso à rota de pedidos.
    return {
        'messagem': 'Você acessou a rota de pedidos.'
    }
