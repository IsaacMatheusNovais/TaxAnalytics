from database import conectar
from fastapi import FastAPI
from fornecedor import criar_fornecedor, listar_fornecedores, buscar_fornecedor_por_cnpj
from models import FornecedorCreate

app = FastAPI()

@app.post("/fornecedor")
def criar_fornecedor_route(fornecedor: FornecedorCreate, status_code=201):
    return criar_fornecedor(fornecedor)

@app.get("/fornecedores")
def listar_fornecedores_route():
    return listar_fornecedores()

@app.get("/fornecedor/{cnpj}")
def buscar_fornecedor_route(cnpj: str):
    return buscar_fornecedor_por_cnpj(cnpj)
