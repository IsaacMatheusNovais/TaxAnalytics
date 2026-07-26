from fastapi import FastAPI, UploadFile, File # Classe necessária para reber arquivo pelo endpoint.
from fornecedor import criar_fornecedor, listar_fornecedores, buscar_fornecedor_por_cnpj, atualizar_fornecedor
from nota_fiscal import buscar_nota_fiscal
from models import FornecedorCreate, FornecedorUpdate, UsuarioCreate
from importacao import importar_xml
from pathlib import Path
from usuario import criar_usuario

app = FastAPI()

#endpoint para criar fornecedor.
@app.post("/fornecedor")
def criar_fornecedor_route(fornecedor: FornecedorCreate, status_code=201):
    return criar_fornecedor(fornecedor)

#endpoint para listar fornecedores
@app.get("/fornecedores")
def listar_fornecedores_route():
    return listar_fornecedores()

#endpoint para buscar fornecedor pelo CNPJ
@app.get("/fornecedor/{cnpj}")
def buscar_fornecedor_route(cnpj: str):
    return buscar_fornecedor_por_cnpj(cnpj)

#endpoint para atualizar fornecedor
@app.put("/fornecedor/{cnpj}")
def atualizar_fornecedor_route(cnpj: str, fornecedor: FornecedorUpdate):
    return atualizar_fornecedor(cnpj, fornecedor)

#endpoint para buscar nota fiscal pelo numero, serie e cnpj
@app.get("/nota_fiscal/{numero}/{serie}/{cnpj}")
def buscar_nota_fiscal_route(numero: str, serie: str, cnpj:str):
    return buscar_nota_fiscal(numero, serie, cnpj)

# Endpoint responsável por receber um arquivo XML enviado pelo usuário.
@app.post("/importar-xml")
async def importar_xml_route(arquivos: list[UploadFile] = File(...)): # Os 3 pontos significa que o arquivo é obrigatório.

    resultados = []
    erros = 0
    sucessos = 0

    for arquivo in arquivos:
        caminho_arquivo = Path("xmls") / arquivo.filename

        with open(caminho_arquivo, "wb") as file:
            conteudo = await arquivo.read()
            file.write(conteudo)

        try:
            resultado = importar_xml(caminho_arquivo)
            resultados.append({
                "arquivo": arquivo.filename,
                "resultado": resultado})
            sucessos += 1
        except Exception as error:
            resultado = {
                "success": False,
                "message": str(error)
            }

            resultados.append({
                "arquivo": arquivo.filename,
                "resultado": resultado
            })

            erros += 1
        finally:
            caminho_arquivo.unlink(missing_ok=True)

    return {
        "success": erros == 0,
        "arquivos_recebidos": len(arquivos),
        "arquivos_processados": len(resultados),
        "sucessos": sucessos,
        "erros": erros,
        "resultados": resultados
    }

# Endpoint para criar usuario
@app.post("/usuario")
def criar_usuario_route(usuario: UsuarioCreate):
    return criar_usuario(usuario)