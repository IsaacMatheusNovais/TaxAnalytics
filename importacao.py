from pathlib import Path
from models import FornecedorCreate, NotaFiscalCreate, ItemNotaCreate
from importador_xml import ler_xml
from fornecedor import buscar_fornecedor_por_cnpj, criar_fornecedor
from nota_fiscal import buscar_nota_fiscal, criar_nota_fiscal
from item_nota import criar_item_nota

def importar_xml(caminho_arquivo: Path):
    dados = ler_xml(caminho_arquivo)

    fornecedor = dados["fornecedor"]
    nota_fiscal = dados["nota_fiscal"]

    # Verifica se o fornecedor já existe
    fornecedor_existente = buscar_fornecedor_por_cnpj(fornecedor["cnpj"])

    if fornecedor_existente["success"]:
        pass #não faz nada, segue o fluxo.
    else:
        novo_fornecedor = FornecedorCreate(**fornecedor) # As duas estrelas '**' pega cada chave do dicionário e a transforma em um parâmetro nomeado.
        # A linha acima serve para transformar o dicionário retornado pela função extrair_fornecedor() que está sendo chamada dentro da função ler_xml() em um objeto da classe FornecedorCreate.
        fornecedor_criado = criar_fornecedor(novo_fornecedor) #Pega o objeto criado e cadastra um novo fornecedor reutilizando nossa função que foi importada.

        if not fornecedor_criado["success"]:
            return fornecedor_criado
    
    # Reutiliza o dado cnpj do dicionário fornecedor para o dicionário da nota fiscal já que em ler_xml a função extrair_nota não coleta o cnpj novamente uma vez que já foi feito por extrair_fornecedor.
    nota_fiscal["cnpj"] = fornecedor["cnpj"]

    #verifica se a nota já existe
    nota_fiscal_existente = buscar_nota_fiscal(nota_fiscal["numero"], nota_fiscal["serie"], nota_fiscal["cnpj"])

    if nota_fiscal_existente["success"]:
        # A nota já existe no banco, então apenas recuperamos seu id para utilizar no cadastro dos itens.
        id_nota = nota_fiscal_existente["nota_fiscal"]["id_nota"]

    else:
        # A nota não existe, então transformamos o dicionário em um objeto NotaFiscalCreate.
        nova_nota_fiscal = NotaFiscalCreate(**nota_fiscal)

        # Cadastra a nota fiscal no banco de dados.
        nota_fiscal_criada = criar_nota_fiscal(nova_nota_fiscal)

        # Se ocorrer algum erro no cadastro, interrompe a importação e retorna o erro.
        if not nota_fiscal_criada["success"]:
            return nota_fiscal_criada

        # Se o cadastro foi realizado com sucesso, recuperamos o id gerado pelo banco.
        id_nota = nota_fiscal_criada["id_nota"]

    # Coloca o dicionário de itens retornado pela função ler_xml dentro da variável itens.
    itens = dados["itens"]

    for item in itens:
        item["id_nota"] = id_nota # Para cada item na nota, este comando insere no índice 0 do dicionário de informações do item o id da nota fiscal a qual ele pertence.

        novo_item = ItemNotaCreate(**item) #Transforma o dicionário em um objeto da classe ItemNotaCreate

        novo_item_adicionado = criar_item_nota(novo_item) # Chama a função para criar um novo item apartir do objeto recebido
        
        if not novo_item_adicionado["success"]:# Verifica se o item foi devidamente criado
            return novo_item_adicionado # Se não foi criado, retorna a mensagem de erro da função
    return {
    "success": True,
    "message": "XML importado com sucesso.",
    "id_nota": id_nota,
    "total_itens": len(itens)
}

        

arquivo = Path("xmls/NFE-31250420381877000420550000000497831193965250.xml") #nota ta tetra
resultado = importar_xml(arquivo)
print (resultado)