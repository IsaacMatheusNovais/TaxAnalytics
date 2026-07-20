from database import conectar
from models import ItemNotaCreate

def criar_item_nota(item: ItemNotaCreate):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO item_nota
                        (item_descricao, quantidade,
                         unidade_medida, valor_unitario,
                         id_nota)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        item.item_descricao,
                        item.quantidade,
                        item.unidade_medida,
                        item.valor_unitario,
                        item.id_nota,
                    ),
                )
                conexao.commit()
                return{
                    "success": True,
                    "message": "Item cadastrado com sucesso"
                }
    except Exception as error:
        if conexao is not None:
            conexao.rollback()
            return{
                "success": False,
                "message": f"Erro ao cadastrar item: {error}",
                "type": type(error).__name__
            }
        return{
            "success": False,
            "message": f"Erro ao conectar no banco de dados: {error}",
            "type": type(error).__name__
        }

