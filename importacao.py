from pathlib import Path
from models import FornecedorCreate
from importador_xml import ler_xml
from fornecedor import buscar_fornecedor_por_cnpj, criar_fornecedor
from nota_fiscal import buscar_nota_fiscal, criar_nota_fiscal

def importar_xml(caminho_arquivo: Path):
    dados = ler_xml(caminho_arquivo)

    fornecedor = dados["fornecedor"]
    nota_fiscal = dados["nota_fiscal"]

    fornecedor_existente = buscar_fornecedor_por_cnpj(fornecedor["cnpj"])

    if fornecedor_existente["success"]:
        pass #não faz nada, segue o fluxo.
    else:
        novo_fornecedor = FornecedorCreate(**fornecedor) # As duas estrelas '**' pega cada chave do dicionário e a transforma em um parâmetro nomeado.
        # A linha acima serve para transformar o dicionário retornado pela função extrair_fornecedor() que está sendo chamada dentro da função ler_xml() em um objeto da classe FornecedorCreate.
        resultado = criar_fornecedor(novo_fornecedor) #Pega o objeto criado e cadastra um novo fornecedor reutilizando nossa função que foi importada.

        if not resultado["success"]:
            return resultado
        
        #lembrar de decidir de onde virá o path, se vamos testar a função agora com outra nota, ou se vamos já montar a 
        # função pra receber o xml pelo endpoint e deixar pra testar ela lá na frente.
    
    nota_fiscal_existente = buscar_nota_fiscal(nota_fiscal["numero"], nota_fiscal["serie"], nota_fiscal["cnpj"])

    if nota_fiscal_existente["seccess"]:
        pass
    else:
        

arquivo = Path("xmls/NFE-31250420381877000420550000000497831193965250.xml") #nota ta tetra
importar_xml(arquivo)