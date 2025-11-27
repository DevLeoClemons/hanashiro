CREATE TABLE cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf_cnpj TEXT,
    telefone TEXT,
    email TEXT,
    endereco TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE fornecedor (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT,
    email TEXT,
    telefone TEXT,
    endereco TEXT,
    contato_responsavel TEXT
);
CREATE TABLE produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT,
    descricao TEXT,
    preco_unitario REAL,
    quantidade_estoque INTEGER DEFAULT 0,
    id_fornecedor INTEGER,
    FOREIGN KEY(id_fornecedor) REFERENCES fornecedor(id_fornecedor)
);
CREATE TABLE pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    data_pedido TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    valor_total REAL,
    FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);
CREATE TABLE item_pedido (
    id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER,
    id_produto INTEGER,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL,
    subtotal REAL,
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto)
);
CREATE TABLE pregao (
    id_pregao INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_edital TEXT,
    descricao TEXT,
    data_publicacao TEXT,
    data_limite TEXT,
    status TEXT,
    arquivo_edital TEXT,
    id_orgao INTEGER,
    FOREIGN KEY(id_orgao) REFERENCES orgao_publico(id_orgao)
);
CREATE TABLE orgao_publico (
    id_orgao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_orgao TEXT NOT NULL,
    cnpj TEXT,
    email_contato TEXT,
    telefone TEXT,
    endereco TEXT
);
CREATE TABLE caracteristica_tecnica (
    id_caracteristica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produto INTEGER,
    nome_caracteristica TEXT NOT NULL,
    valor_caracteristica TEXT,
    FOREIGN KEY(id_produto) REFERENCES produto(id_produto) ON DELETE CASCADE
);
CREATE TABLE contato_fornecedor (
    id_contato INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fornecedor INTEGER,
    id_pedido INTEGER,
    data_contato TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    observacao TEXT,
    arquivo_resposta TEXT,
    FOREIGN KEY(id_fornecedor) REFERENCES fornecedor(id_fornecedor),
    FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
);
