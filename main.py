from database import conectar
from fastapi import FastAPI
from fornecedor import criar_fornecedor, listar_fornecedores, buscar_fornecedor_por_cnpj, atualizar_fornecedor
from nota_fiscal import buscar_nota_fiscal
from models import FornecedorCreate, FornecedorUpdate

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
