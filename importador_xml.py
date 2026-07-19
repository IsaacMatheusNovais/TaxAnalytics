from pathlib import Path
import xml.etree.ElementTree as ET

arquivo = Path("xmls/NFE-35250416797826000163550010000398631019270599.xml") #nota Gledson

def ler_xml(caminho_arquivo: Path):
    arvore = ET.parse(caminho_arquivo)
    raiz = arvore.getroot()

    # Namespace utilizado pelo XML da NF-e.
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    fornecedor = extrair_fornecedor(raiz, ns)
    nota_fiscal = extrair_nota_fiscal(raiz, ns)
    itens = extrair_produtos(raiz, ns)

    return {
        "fornecedor": fornecedor,
        "nota_fiscal": nota_fiscal,
        "itens": itens
    }

def extrair_fornecedor(raiz, ns):

    nfe = raiz.find("nfe:NFe", ns)  # Da 1° para a 2° camada (Raiz > NFe).
    inf_nfe = nfe.find("nfe:infNFe", ns)  # Da 2° para a 3° camada (NFe > infNFe).

    emitente = inf_nfe.find("nfe:emit", ns)  # Adentra o bloco do emitente da nota.

    cnpj = emitente.find("nfe:CNPJ", ns)  # Coleta o CNPJ do emitente.
    razao_social = emitente.find("nfe:xNome", ns)  # Coleta a razão social do emitente.

    return {
        "cnpj": cnpj.text,
        "razao_social": razao_social.text,

        # O XML da NF-e também não informa o nome fantasia.
        # Por enquanto utilizamos a razão social.
        "nome_fantasia": razao_social.text
    }

def extrair_nota_fiscal(raiz, ns):

    nfe = raiz.find("nfe:NFe", ns)  # Da 1° para a 2° camada (Raiz > NFe).
    inf_nfe = nfe.find("nfe:infNFe", ns)  # Da 2° para a 3° camada (NFe > infNFe).

    ide = inf_nfe.find("nfe:ide", ns)  # Adentra o bloco de identificação da nota.

    numero = ide.find("nfe:nNF", ns)  # Coleta o número da nota.
    serie = ide.find("nfe:serie", ns)  # Coleta a série da nota.
    data_emissao = ide.find("nfe:dhEmi", ns)  # Coleta a data de emissão.

    total = inf_nfe.find("nfe:total", ns)  # Adentra o bloco de totais da nota.
    icms_tot = total.find("nfe:ICMSTot", ns)  # Adentra o bloco ICMSTot.

    valor_produtos = icms_tot.find("nfe:vProd", ns)  # Valor total dos produtos.
    valor_frete = icms_tot.find("nfe:vFrete", ns)  # Valor do frete.
    valor_desconto = icms_tot.find("nfe:vDesc", ns)  # Valor do desconto.
    valor_total = icms_tot.find("nfe:vNF", ns)  # Valor total da nota.

    return {
        "numero": numero.text,
        "serie": serie.text,
        "data_emissao": data_emissao.text,
        "valor_produtos": valor_produtos.text,
        "valor_frete": valor_frete.text,
        "valor_desconto": valor_desconto.text,
        "valor_total": valor_total.text
    }

def extrair_produtos(raiz, ns):
     
    nfe = raiz.find("nfe:NFe", ns)  # Da 1° para a 2° camada (Raiz > NFe).
    inf_nfe = nfe.find("nfe:infNFe", ns)  # Da 2° para a 3° camada (NFe > infNFe).
    detalhes = inf_nfe.findall("nfe:det", ns) # Captura todos os "detalhes" que são todas as informações de cada item.

    itens = []

    for detalhe in detalhes: # Percorre todos os item da nota.

        produto = detalhe.find("nfe:prod", ns) # Adentra o bloco de informações do produto do item atual.
        item_descricao = produto.find("nfe:xProd", ns) # Recebe a descrição do produto atual no laço for.
        unidade_medida = produto.find("nfe:uCom", ns) # Recebe a unidade de medida do produto atual no laço for.
        quantidade = produto.find("nfe:qCom", ns) # Recebe a quantidade do produto atual no laço for.
        valor_unitario = produto.find("nfe:vUnCom", ns) # Recebe o valor unitário do produto atual no laço for.

        itens.append({ # Captura todos os itens atuais do loop, transforma em um dicionário e os adiciona na lista itens.
        "item_descricao": item_descricao.text,
        "quantidade": quantidade.text,
        "unidade_medida": unidade_medida.text,
        "valor_unitario": valor_unitario.text
        })
    return itens

# Ative esta linha para testar as funções acima e imprimir suas saidas.
#ler_xml(arquivo)