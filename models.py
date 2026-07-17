from pydantic import BaseModel

#classse utilizada para criar fornecedores
class FornecedorCreate(BaseModel):
    cnpj: str #cada campo deste é um objeto da classe Fornecedor create.
    razao_social: str
    nome_fantasia: str

#classe utilizada para atualizar fornecedores
class FornecedorUpdate(BaseModel):
    razao_social: str #cada campo deste é um objeto da classe Fornecedor update.
    nome_fantasia: str
