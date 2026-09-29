-- =========================================================
-- BANCO DE DADOS DA LOJA RHIZEL
-- Execute este arquivo no MySQL Workbench.
-- =========================================================

CREATE DATABASE IF NOT EXISTS rhizel_loja
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE rhizel_loja;

-- ---------------------------------------------------------
-- PRODUTOS
-- Guarda as informações principais de cada produto.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
-- IMAGENS
-- Guarda somente o caminho da foto.
-- A foto física fica em static/imagens/.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS imagens_produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    caminho VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (produto_id)
        REFERENCES produtos(id)
        ON DELETE CASCADE
);

-- ---------------------------------------------------------
-- TAMANHOS
-- Nesta primeira versão, os tamanhos ficam diretamente
-- relacionados ao produto.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS produto_tamanhos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    tamanho VARCHAR(10) NOT NULL,

    FOREIGN KEY (produto_id)
        REFERENCES produtos(id)
        ON DELETE CASCADE
);

-- ---------------------------------------------------------
-- VENDAS
-- Representa uma compra finalizada.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total DECIMAL(10, 2) NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
-- ITENS DA VENDA
-- Guarda quais produtos fizeram parte de cada venda.
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS itens_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT NOT NULL,
    produto_id INT NOT NULL,
    tamanho VARCHAR(10) NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,

    FOREIGN KEY (venda_id)
        REFERENCES vendas(id)
        ON DELETE CASCADE,

    FOREIGN KEY (produto_id)
        REFERENCES produtos(id)
);

-- Conferência final:
SHOW TABLES;
