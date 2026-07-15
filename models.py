from pydantic import BaseModel

class FornecedorCreate(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: str
