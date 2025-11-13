# Importa o APIRouter (para organizar rotas), Depends (para injeção de dependências)
# e Session (para gerenciar a conexão com o banco de dados via SQLAlchemy).
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importa a função que cria uma nova sessão de banco a cada requisição.
from dependencies import pegar_sessao

# Importa os esquemas Pydantic usados para validação de entrada.
from schemas import PedidoSchema, LoginSchema

# Importa o modelo Pedido, que representa a tabela de pedidos no banco de dados.
from models import Pedido


# Cria um roteador específico para rotas de pedidos.
# - prefix: todas as rotas começam com "/orders".
# - tags: define o agrupamento no Swagger UI (/docs).
order_router = APIRouter(prefix='/orders', tags=['orders'])


# ==========================================================
# 📦 ROTA GET — Rota padrão (exemplo) para pedidos
# ==========================================================
@order_router.get('/')
async def pedidos():
    '''
    Essa é a rota padrão de pedidos do nosso sistema.

    Em um cenário real, esta rota poderia:
      - retornar todos os pedidos de um usuário autenticado;
      - permitir filtros (por status, data, cliente, etc.);
      - exigir autenticação (com JWT ou OAuth2).

    Aqui, é apenas um ponto de entrada ilustrativo.
    '''

    return {
        'messagem': 'Você acessou a rota de pedidos.'
    }


# ==========================================================
# 🧾 ROTA POST — Criação de um novo pedido
# ==========================================================
@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    '''
    Cria um novo pedido no banco de dados.

    Parâmetros esperados (via corpo da requisição):
    - usuario: ID do usuário associado ao pedido.
    - status (opcional): estado atual do pedido (ex: "PENDENTE", "FINALIZADO").
    - preco (opcional): valor total do pedido.

    A sessão de banco é injetada automaticamente via Depends(pegar_sessao),
    garantindo abertura e fechamento corretos da conexão.
    '''

    # Cria uma nova instância de Pedido usando os dados do schema.
    novo_pedido = Pedido(usuario=pedido_schema.usuario)

    # Adiciona o pedido à sessão (ainda não grava no banco).
    session.add(novo_pedido)

    # Grava as alterações no banco (INSERT efetivo).
    session.commit()

    # Retorna uma resposta de sucesso com o ID gerado do pedido.
    return {'message': f'Pedido criado com sucesso. ID do pedido: {novo_pedido.id}'}
