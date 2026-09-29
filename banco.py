import os
from decimal import Decimal
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    """Abre uma conexão com o banco MySQL usando as variáveis do .env."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "rhizel_loja"),
    )


def criar_produto(nome, preco, descricao, tamanhos):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO produtos (nome, preco, descricao)
            VALUES (%s, %s, %s)
            """,
            (nome, preco, descricao),
        )

        produto_id = cursor.lastrowid

        for tamanho in tamanhos:
            cursor.execute(
                """
                INSERT INTO produto_tamanhos (produto_id, tamanho)
                VALUES (%s, %s)
                """,
                (produto_id, tamanho),
            )

        conexao.commit()
        return produto_id

    finally:
        cursor.close()
        conexao.close()


def adicionar_imagem(produto_id, caminho):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO imagens_produto (produto_id, caminho)
            VALUES (%s, %s)
            """,
            (produto_id, caminho),
        )
        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                p.id,
                p.nome,
                p.preco,
                p.descricao,
                (
                    SELECT i.caminho
                    FROM imagens_produto i
                    WHERE i.produto_id = p.id
                    ORDER BY i.id
                    LIMIT 1
                ) AS imagem
            FROM produtos p
            ORDER BY p.id DESC
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conexao.close()


def buscar_produto(produto_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nome, preco, descricao
            FROM produtos
            WHERE id = %s
            """,
            (produto_id,),
        )

        produto = cursor.fetchone()

        if produto is None:
            return None

        cursor.execute(
            """
            SELECT caminho
            FROM imagens_produto
            WHERE produto_id = %s
            ORDER BY id
            """,
            (produto_id,),
        )

        produto["imagens"] = [linha["caminho"] for linha in cursor.fetchall()]

        cursor.execute(
            """
            SELECT tamanho
            FROM produto_tamanhos
            WHERE produto_id = %s
            ORDER BY id
            """,
            (produto_id,),
        )

        produto["tamanhos"] = [linha["tamanho"] for linha in cursor.fetchall()]

        return produto

    finally:
        cursor.close()
        conexao.close()


def criar_venda(carrinho, total):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO vendas (total)
            VALUES (%s)
            """,
            (total,),
        )

        venda_id = cursor.lastrowid

        for item in carrinho:
            subtotal = Decimal(str(item["preco"])) * item["quantidade"]

            cursor.execute(
                """
                INSERT INTO itens_venda
                (venda_id, produto_id, tamanho, quantidade, preco_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    venda_id,
                    item["produto_id"],
                    item["tamanho"],
                    item["quantidade"],
                    item["preco"],
                    subtotal,
                ),
            )

        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, total, data_venda
            FROM vendas
            ORDER BY id DESC
            """
        )

        vendas = cursor.fetchall()

        for venda in vendas:
            cursor.execute(
                """
                SELECT
                    iv.tamanho,
                    iv.quantidade,
                    iv.preco_unitario,
                    iv.subtotal,
                    p.nome
                FROM itens_venda iv
                INNER JOIN produtos p ON p.id = iv.produto_id
                WHERE iv.venda_id = %s
                """,
                (venda["id"],),
            )

            venda["itens"] = cursor.fetchall()

        return vendas

    finally:
        cursor.close()
        conexao.close()


def limpar_vendas():
    """Mantida para estudos futuros; não é usada no fluxo principal."""
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("DELETE FROM vendas")
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()
