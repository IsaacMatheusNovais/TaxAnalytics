from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

#classse utilizada para criar fornecedores
class FornecedorCreate(BaseModel):
    cnpj: str #cada campo deste é um objeto da classe Fornecedor create.
    razao_social: str
    nome_fantasia: str

#classe utilizada para atualizar fornecedores
class FornecedorUpdate(BaseModel):
    razao_social: str #cada campo deste é um objeto da classe Fornecedor update.
    nome_fantasia: str

class NotaFiscalCreate(BaseModel):
    numero: str
    serie: str
    data_emissao: datetime
    valor_produtos: Decimal #Para lidar com valores o tipo de dado correto no pydantic é o Decimal
    valor_frete: Decimal
    valor_desconto: Decimal
    valor_total: Decimal
    cnpj: str

class ItemNotaCreate(BaseModel):
    item_descricao: str
    quantidade: Decimal
    unidade_medida: str
    valor_unitario: Decimal
    id_nota: int
