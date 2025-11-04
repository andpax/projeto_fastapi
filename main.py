# Importa a classe FastAPI, que é o núcleo do framework.
# Ela permite criar e gerenciar toda a aplicação web.
from fastapi import FastAPI


# Cria uma instância da aplicação FastAPI.
# Essa variável "app" representa a aplicação em si, 
# e é por meio dela que configuramos rotas, middlewares, eventos, etc.
app = FastAPI()


# Importa os módulos de rotas personalizadas.
# Cada arquivo (auth_routes e order_routes) provavelmente contém
# rotas organizadas por funcionalidade (autenticação e pedidos, por exemplo).
from auth_routes import auth_router
from order_routes import order_router


# Inclui os "routers" na aplicação principal.
# Isso permite que as rotas definidas em outros módulos sejam registradas
# na aplicação principal, mantendo o código modular e organizado.
app.include_router(auth_router)   # Rotas relacionadas à autenticação (login, registro, etc.)
app.include_router(order_router)  # Rotas relacionadas a pedidos (criação, listagem, etc.)
