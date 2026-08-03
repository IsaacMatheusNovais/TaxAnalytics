from database import conectar
from psycopg2.extras import RealDictCursor
from models import UsuarioCreate
from seguranca import gerar_hash

def criar_usuario(usuario: UsuarioCreate):
    conexao = None
    try:
        senha_hash = gerar_hash(usuario.senha)
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuario (nome, email,
                    senha_hash, id_nivel) VALUES (%s, %s, %s, %s)""", 
                    (usuario.nome, usuario.email, senha_hash,
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

# Função para buscar usuário por email
def buscar_usuario_por_email(email: str):
    conexao = None
    try:
        with conectar() as conexao:
            with conexao.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""SELECT 
                                usuario.id_usuario,
                                usuario.nome,
                                usuario.email,
                                usuario.senha_hash,
                                usuario.ativo AS status,
                                usuario.criado_em AS criacao,
                                nivel_acesso.descricao AS nivel
                                FROM usuario JOIN nivel_acesso
                                ON usuario.id_nivel = nivel_acesso.id_nivel
                                WHERE usuario.email = %s""", (email,))
                resultado = cursor.fetchone()
                if resultado is None:
                    return {
                        "success": False,
                        "message": "Usuário não encontrado"
                    }
                return{
                    "success": True,
                    "usuario": resultado
                }
    except Exception as error:
        if conexao is not None:
            return{
                "success": False,
                "message": f"Erro ao fazer consulta {error}",
                "type": type(error).__name__
            }
        return{
                "success": False,
                "message": f"Erro ao conectar ao banco de dados {error}",
                "type": type(error).__name__
            }
       
            