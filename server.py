# Importa o servidor ASGI uvicorn, responsável por executar a aplicação FastAPI.
# O Uvicorn é leve, rápido e otimizado para aplicações assíncronas.
import uvicorn


# Esse bloco garante que o código abaixo só será executado
# quando o arquivo for executado diretamente (ex: python run.py).
# Se o módulo for importado por outro script, o servidor NÃO será iniciado automaticamente.
if __name__ == '__main__':
    # Executa o servidor Uvicorn.
    # Parâmetros:
    # - 'main:app': indica o módulo e o nome da instância da aplicação FastAPI (main.py -> app)
    # - host='127.0.0.1': define o endereço local onde o servidor ficará disponível.
    # - port=8000: define a porta do servidor.
    # - reload=True: ativa o "hot reload", ou seja, reinicia o servidor automaticamente ao detectar mudanças no código.
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
