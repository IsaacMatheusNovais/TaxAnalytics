from database import conectar
from psycopg2.extras import RealDictCursor
from models import NotaFiscalCreate

# Função para cadastrar nota fiscal
def criar_nota_fiscal(nota_fiscal: NotaFiscalCreate):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO nota_fiscal (numero,
                    serie, data_emissao, valor_produtos,
                    valor_frete, valor_desconto, valor_total, cnpj)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_nota""",
                    (nota_fiscal.numero,
                    nota_fiscal.serie,
                    nota_fiscal.data_emissao,
                    nota_fiscal.valor_produtos,
                    nota_fiscal.valor_frete,
                    nota_fiscal.valor_desconto,
                    nota_fiscal.valor_total,
                    nota_fiscal.cnpj))
                id_nota = cursor.fetchone()[0]
                conexao.commit()
                return{
                    "success": True,
                    "message": "Nota fiscal cadastrada com sucesso.",
                    "id_nota": id_nota
                }
    except Exception as error:
        if conexao is not None:
            conexao.rollback()

            return {
                "success": False,
                "message": f"Erro ao cadastrar nota fiscal: {error}",
                "type": type(error).__name__
            }

        return {
            "success": False,
            "message": f"Erro ao conectar ao banco de dados: {error}",
            "type": type(error).__name__
        }


#função para buscar uma nota fiscal pelo numero + serie +cnpj
def buscar_nota_fiscal(numero, serie, cnpj):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""SELECT numero, serie, cnpj
                               FROM nota_fiscal WHERE numero = %s AND
                               serie = %s AND cnpj = %s """, (numero, serie, cnpj,))
                nota_fiscal = cursor.fetchone()
                if nota_fiscal:
                    return{
                        "success": True,
                        "nota_fiscal": nota_fiscal  
                    }
                else:
                    return{
                        "success": False,
                        "message": "Nota fiscal não encontrada"
                    }
    except Exception as error:
        if conexao is not None:
            return{
                "success": False,
                "message": f"Erro ao buscar nota fiscal: {error}",
                "type": type(error).__name__
            }
        return{
            "success": False,
            "message": f"Erro ao conectar ao banco de dados: {error}",
            "type": type(error).__name__
        }
