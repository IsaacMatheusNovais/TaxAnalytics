from pydantic import BaseModel, EmailStr, Field
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

#Classe utilizada para registrar nota fiscal no banco
class NotaFiscalCreate(BaseModel):
    numero: str
    serie: str
    data_emissao: datetime
    valor_produtos: Decimal #Para lidar com valores o tipo de dado correto no pydantic é o Decimal
    valor_frete: Decimal
    valor_desconto: Decimal
    valor_total: Decimal
    cnpj: str

#classe utilizada para registrar item da nota no banco
class ItemNotaCreate(BaseModel):
    item_descricao: str
    quantidade: Decimal
    unidade_medida: str
    valor_unitario: Decimal
    id_nota: int

#classe utilizada para criar usuários
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=8) #Usa palavra reservada Field da bibioteca pydantic
    id_nivel: str

#classe utilizada para criar login de usuários
class UsuarioLogin(BaseModel):
    usuario: str
    senha: str = Field(min_length=8)

#classe utilizada para atualizar usuários
class UsuarioUpdate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=8)
    ativo: bool

#classe utilizada para criar níveis de acesso
class NivelAcessoCreate(BaseModel):
    descricao: str

#classe utilizada para requisição de login
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str
