Perfeito, banco criado e esta é a estrutura:

CREATE TABLE fornecedor(
	cnpj CHAR(14) PRIMARY KEY
	CHECK (cnpj ~ '^[0-9]+$'),
	razao_social VARCHAR(100) NOT NULL,
	nome_fantasia VARCHAR(100) NOT NULL
)

CREATE TABLE status (
	id_status SERIAL PRIMARY KEY,
	descricao VARCHAR(15) NOT NULL
)

CREATE TABLE nota_fiscal(
	id_nota SERIAL PRIMARY KEY,
	numero VARCHAR(20) NOT NULL
	CHECK (numero ~ '^[0-9]+$'),
	serie VARCHAR(3) NOT NULL
	CHECK (serie ~ '^[0-9]{1,3}$'),
	data_emissao TIMESTAMP WITH TIME ZONE NOT NULL,
	valor_produtos DECIMAL(15,2) NOT NULL,
	valor_frete DECIMAL(15,2) NOT NULL DEFAULT 0,
	valor_desconto DECIMAL(15,2) NOT NULL DEFAULT 0,
	valor_total DECIMAL(15,2) NOT NULL,
	id_status SMALLINT NOT NULL DEFAULT 1,
	FOREIGN KEY (id_status) REFERENCES status(id_status),
	cnpj CHAR(14) NOT NULL,
	FOREIGN KEY (cnpj) REFERENCES fornecedor(cnpj)
)

CREATE TABLE item_nota(
	id_item SERIAL PRIMARY KEY,
	item_descricao VARCHAR(100) NOT NULL,
	quantidade DECIMAL(10,3) NOT NULL,
	unidade_medida VARCHAR(10) NOT NULL,
	valor_unitario DECIMAL(10,2) NOT NULL,
	id_nota INT NOT NULL,
	FOREIGN KEY (id_nota) REFERENCES nota_fiscal(id_nota)
)

CREATE ROLE sistema_notas
LOGIN
PASSWORD '31415926536Pi#';

GRANT ALL PRIVILEGES
ON DATABASE automação_nfs
TO sistema_notas;