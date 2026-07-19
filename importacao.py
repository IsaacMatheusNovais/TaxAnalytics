from pathlib import Path
from models import FornecedorCreate, NotaFiscalCreate
from importador_xml import ler_xml
from fornecedor import buscar_fornecedor_por_cnpj, criar_fornecedor
from nota_fiscal import buscar_nota_fiscal, criar_nota_fiscal

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
            item["id_nota"] = id_nota #Essa linha significa: "Crie (ou atualize) a chave id_nota do dicionário item com o valor da variável id_nota."
            

        

arquivo = Path("xmls/NFE-31250420381877000420550000000497831193965250.xml") #nota ta tetra
importar_xml(arquivo)