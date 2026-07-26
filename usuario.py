from database import conectar
from psycopg2.extras import RealDictCursor
from models import UsuarioCreate

def criar_usuario(usuario: UsuarioCreate):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuario (nome, email,
                    senha_hash, id_nivel) VALUES (%s, %s, %s, %s)""", 
                    (usuario.nome, usuario.email, usuario.senha,
                    usuario.id_nivel)
                )
                conexao.commit()
                return{
                    "success": True,
                    "message": "Usuario cadastrado com sucesso",
                    "data": {
                        "nome": usuario.nome,
                        "email": usuario.email,
                        "nivel": usuario.id_nivel
                    }
                }
    except Exception as error:
        if conexao is not None:
            conexao.rollback()
            return{
                "success": False,
                "message": f"Erro ao cadastrar usuário: {error}",
                "type": type(error).__name__
            }
        return{
            "success": False,
            "message": f"Erro ao conectar ao banco de dados {error}",
            "type": type(error).__name__
        }
         
       
            