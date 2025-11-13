# Importa a classe BaseModel, usada para criar esquemas de validação com o Pydantic.
# Esses esquemas são usados pelo FastAPI para validar e tipar automaticamente os dados recebidos nas requisições.
from pydantic import BaseModel

# Importa o tipo Optional, que permite indicar que um campo pode ser opcional (ou seja, pode ser None).
from typing import Optional


# Define o esquema (modelo) de dados usado para representar o usuário.
# Este schema é usado, por exemplo, ao criar um novo usuário via API.
class UsuarioSchema(BaseModel):
    # Campos obrigatórios: nome, email e senha.
    nome: str
    email: str
    senha: str

    # Campos opcionais: ativo e admin.
    # Por serem Optional, o cliente pode omitir esses valores ao enviar a requisição.
    ativo: Optional[bool]
    admin: Optional[bool]

    # Configurações adicionais do Pydantic.
    class Config:
        # Permite que o schema converta automaticamente objetos ORM (como instâncias de modelos SQLAlchemy)
        # para esse formato Pydantic. É útil ao retornar dados diretamente do banco de dados.
        from_attributes = True



class PedidoSchema(BaseModel):
    # ID do usuário responsável pelo pedido.
    # Esse campo deve existir no banco de dados (tabela 'usuarios').
    usuario: int

    # Configuração extra do Pydantic.
    # 'from_attributes = True' permite criar o schema a partir de objetos ORM (como modelos SQLAlchemy).
    class Config:
        from_attributes = True



class LoginSchema(BaseModel):
    # E-mail do usuário, usado como identificador único para login.
    email: str

    # Senha do usuário em texto puro (será comparada com a senha criptografada no banco).
    senha: str

    class Config:
        # Permite converter automaticamente objetos ORM (SQLAlchemy) em modelos Pydantic.
        from_attributes = True