from database import conectar
from models import FornecedorCreate
from psycopg2.extras import RealDictCursor

#função criar fornecedor
def criar_fornecedor(fornecedor: FornecedorCreate): #Type hint avisando que a função deve reber um objeto "fornecedor" do tipo FornecedorCreate.
    conexao = None #define um valor nulo para a variável conexao.
    try:
        with conectar() as conexao: #em caso de sucesso, a função conectar() retorna uma conexão com o banco de dados e a variável conexao recebe essa conexão.
            with conexao.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO fornecedor (cnpj, razao_social, nome_fantasia) VALUES (%s, %s, %s)""",
                    (fornecedor.cnpj, fornecedor.razao_social, fornecedor.nome_fantasia)
                )
                conexao.commit() #comita e confirma a transação, salvando as alterações no banco de dados.
                return {
                    "success": True,
                    "message": "Fornecedor cadastrado com sucesso",
                    "data": {
                        "cnpj": fornecedor.cnpj
                    }
                }
    except Exception as error: #"coleta" o erro que ocorreu durante a execução do código
        if conexao is not None: #se a variável conexao não for nula, significa que a conexão com o banco de dados foi estabelecida com sucesso.
            conexao.rollback() #desfaz qualquer alteração feita no banco de dados durante a transação atual.
            return {
                "success": False,
                "message": f"Erro ao cadastrar fornecedor: {error}",
                "type": type(error).__name__ #retorna o tipo de erro que ocorreu.
            }
        return { #caso a conexão com o banco de dados não tenha sido estabelecida...
            "success": False,
            "message": f"Erro ao conectar ao banco de dados: {error}", #Notifica o erro e o tipo de erro que ocorreu.
            "type": type(error).__name__
        }
    
#função listar fornecedores
def listar_fornecedores():
    conexao = None #define um valor nulo para a variável conexao.
    try:
        with conectar() as conexao: #abaixo utilizando a função RealDictCursor da biblioteca psycopg2.extras para facilitar a visualização dos dados retornados pelo banco. Adiciona "legendas" como: cnpj: 4567789546000125 ao invéz de só o número.
            with conexao.cursor(cursor_factory=RealDictCursor) as cursor:#RealDictCursor permite que os resultados da consulta sejam retornados como dicionários, em vez de tuplas, facilitando o acesso aos dados.
                cursor.execute("""SELECT cnpj, razao_social, nome_fantasia
                                FROM fornecedor ORDER BY razao_social""") #executa a consulta SQL para selecionar os campos cnpj, razao_social e nome_fantasia da tabela fornecedor, ordenando os resultados pelo campo razao_social.
                fornecedores = cursor.fetchall() # Recupera todas as linhas retornadas pela consulta.
                return {
                    "success": True,
                    "fornecedores": fornecedores
                    }
    except Exception as error: #"coleta" o erro que ocorreu durante a execução do código
        if conexao is not None:
            return {
                "success": False,
                "message": f"Erro ao listar fornecedores: {error}",
                "type": type(error).__name__
            }
        return {
            "success": False,
            "message": f"Erro ao conectar ao banco de dados: {error}",
            "type": type(error).__name__
        }
    
#FUNÇÃO PARA BUSCAR FORNECEDOR PELO CNPJ
def buscar_fornecedor_por_cnpj(cnpj: str):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """SELECT cnpj, razao_social, nome_fantasia
                    FROM fornecedor WHERE cnpj = %s""",
                    (cnpj,)
                )
                fornecedor = cursor.fetchone()
                if fornecedor:
                    return {
                        "success": True,
                        "fornecedor": fornecedor
                    }
                else:
                    return {
                        "success": False,
                        "message": "Fornecedor não encontrado"
                    }
    except Exception as error:
        if conexao is not None:
            return {
                "success": False,
                "message": f"Erro ao buscar fornecedor: {error}",
                "type": type(error).__name__
            }
        return {
            "success": False,
            "message": f"Erro ao conectar ao banco de dados: {error}",
            "type": type(error).__name__
        }