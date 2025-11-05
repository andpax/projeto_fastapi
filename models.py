# Importa os principais componentes do SQLAlchemy.
# - create_engine: cria a conexão com o banco de dados.
# - Column, String, Integer, Boolean, Float, ForeignKey: usados para definir colunas nas tabelas.
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey

# Importa o 'declarative_base', usado para criar classes mapeadas como tabelas do banco.
from sqlalchemy.orm import declarative_base

# Importa o tipo ChoiceType (opcional), útil para criar colunas com valores limitados (como enums).
from sqlalchemy_utils.types import ChoiceType


# Cria a conexão com o banco de dados SQLite chamado 'banco.db'.
# O formato 'sqlite:///banco.db' indica que o banco será criado/localizado no mesmo diretório do projeto.
db = create_engine('sqlite:///banco.db')

# Cria a classe base para todas as tabelas do banco.
# Todas as classes que herdarem de 'Base' serão mapeadas como tabelas.
Base = declarative_base()


# ===========================
# 🧑‍💻 Tabela: USUARIOS
# ===========================
class Usuario(Base):
    # Define o nome da tabela no banco de dados.
    __tablename__ = 'usuarios'

    # Criação das colunas da tabela.
    id = Column('id', Integer, primary_key=True, autoincrement=True)  # Chave primária
    nome = Column('nome', String)                                     # Nome do usuário
    email = Column('email', String, nullable=False)                   # Email obrigatório
    senha = Column('senha', String)                                   # Senha de acesso
    ativo = Column('ativo', Boolean)                                  # Indica se o usuário está ativo
    admin = Column('admin', Boolean, default=False)                   # Indica se é administrador

    # Construtor da classe: define os atributos ao criar um novo objeto.
    def __init__(self, nome, email, senha, ativo, admin):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    

# ===========================
# 📦 Tabela: PEDIDOS
# ===========================
class Pedido(Base):
    __tablename__ = 'pedidos'

    # Exemplo de valores possíveis para status (comentado por enquanto).
    # Útil quando se quer restringir os valores possíveis da coluna.
    # STATUS_PEDIDOS = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO')
    # )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    # status = Column('status', ChoiceType(choices=STATUS_PEDIDOS))  # Exemplo usando ChoiceType
    status = Column('status', String)                                 # Status do pedido (texto simples)
    usuario = Column('usuario', ForeignKey('usuarios.id'))            # FK: referência ao usuário que fez o pedido
    preco = Column('preco', Float)                                    # Valor total do pedido

    # Construtor da classe Pedido.
    # Define o usuário que fez o pedido, o status e o preço (por padrão, "PENDENTE" e 0).
    def __init__(self, usuario, status='PENDENTE', preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco
    

# ===========================
# 🍕 Tabela: ITENS DO PEDIDO
# ===========================
class ItensPedido(Base):
    __tablename__ = 'itens_pedido'

    id = Column('id', Integer, primary_key=True, autoincrement=True)  # Identificador único
    quantidade = Column('quantidade', Integer)                        # Quantidade do item
    sabor = Column('sabor', String)                                   # Descrição do sabor (ex: pizza)
    tamanho = Column('tamanho', String)                               # Tamanho do item (ex: grande, média)
    preco_unitario = Column('preco_unitario', Float)                  # Preço de uma unidade
    pedido = Column('pedido', ForeignKey('pedidos.id'))               # FK: identifica a qual pedido pertence
    
    # Construtor que define os dados de um item do pedido.
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
