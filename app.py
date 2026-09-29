from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from pathlib import Path
from uuid import uuid4
from decimal import Decimal

from banco import (
    criar_produto,
    listar_produtos,
    buscar_produto,
    adicionar_imagem,
    criar_venda,
    listar_vendas,
    limpar_vendas,
)

app = Flask(__name__)
app.secret_key = "troque-esta-chave-em-producao"

# Pasta onde as fotos enviadas pelo usuário serão salvas.
UPLOAD_FOLDER = Path(app.root_path) / "static" / "imagens"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB por requisição.

EXTENSOES_PERMITIDAS = {"jpg", "jpeg", "png", "webp"}


def extensao_permitida(nome):
    """Verifica se o arquivo possui uma extensão de imagem aceita."""
    return "." in nome and nome.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


@app.route("/")
def index():
    produtos = listar_produtos()
    return render_template("index.html", produtos=produtos)


@app.route("/produto/<int:produto_id>")
def produto(produto_id):
    item = buscar_produto(produto_id)

    if item is None:
        return "Produto não encontrado.", 404

    return render_template("produto.html", produto=item)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    mensagem = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        preco_texto = request.form.get("preco", "").replace(",", ".")
        tamanhos = request.form.getlist("tamanhos")

        if not nome or not preco_texto:
            mensagem = "Preencha o nome e o preço."
            return render_template("cadastrar.html", mensagem=mensagem)

        try:
            preco = Decimal(preco_texto)
            if preco < 0:
                raise ValueError
        except ValueError:
            mensagem = "Informe um preço válido."
            return render_template("cadastrar.html", mensagem=mensagem)

        if not tamanhos:
            mensagem = "Selecione pelo menos um tamanho."
            return render_template("cadastrar.html", mensagem=mensagem)

        # 1. Cria o produto no MySQL e recebe o ID gerado.
        produto_id = criar_produto(nome, preco, descricao, tamanhos)

        # 2. Recebe até 3 fotos diretamente do computador.
        for campo in ("imagem1", "imagem2", "imagem3"):
            arquivo = request.files.get(campo)

            if not arquivo or arquivo.filename == "":
                continue

            if not extensao_permitida(arquivo.filename):
                mensagem = "Use apenas imagens JPG, JPEG, PNG ou WEBP."
                return render_template("cadastrar.html", mensagem=mensagem)

            nome_seguro = secure_filename(arquivo.filename)
            extensao = nome_seguro.rsplit(".", 1)[1].lower()

            # UUID evita que duas fotos com o mesmo nome sobrescrevam uma à outra.
            nome_final = f"{uuid4().hex}.{extensao}"
            caminho = UPLOAD_FOLDER / nome_final
            arquivo.save(caminho)

            # Guardamos no banco apenas o caminho da imagem.
            adicionar_imagem(produto_id, f"imagens/{nome_final}")

        return redirect(url_for("produto", produto_id=produto_id))

    return render_template("cadastrar.html", mensagem=mensagem)


@app.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def adicionar_carrinho(produto_id):
    produto = buscar_produto(produto_id)

    if produto is None:
        return "Produto não encontrado.", 404

    tamanho = request.form.get("tamanho")
    quantidade = int(request.form.get("quantidade", 1))

    if tamanho not in produto["tamanhos"]:
        return "Tamanho inválido.", 400

    if quantidade < 1:
        return "Quantidade inválida.", 400

    carrinho = session.get("carrinho", [])

    carrinho.append({
        "produto_id": produto["id"],
        "nome": produto["nome"],
        "preco": float(produto["preco"]),
        "imagem": produto["imagens"][0] if produto["imagens"] else None,
        "tamanho": tamanho,
        "quantidade": quantidade,
    })

    session["carrinho"] = carrinho
    return redirect(url_for("relatorio"))


@app.route("/relatorio")
def relatorio():
    carrinho = session.get("carrinho", [])

    subtotal = sum(
        Decimal(str(item["preco"])) * item["quantidade"]
        for item in carrinho
    )

    return render_template(
        "relatorio.html",
        carrinho=carrinho,
        subtotal=subtotal,
        total=subtotal,
    )


@app.route("/carrinho/remover/<int:indice>")
def remover_carrinho(indice):
    carrinho = session.get("carrinho", [])

    if 0 <= indice < len(carrinho):
        carrinho.pop(indice)
        session["carrinho"] = carrinho

    return redirect(url_for("relatorio"))


@app.route("/finalizar", methods=["POST"])
def finalizar():
    carrinho = session.get("carrinho", [])

    if not carrinho:
        return redirect(url_for("relatorio"))

    total = sum(
        Decimal(str(item["preco"])) * item["quantidade"]
        for item in carrinho
    )

    criar_venda(carrinho, total)

    session["carrinho"] = []
    return render_template("finalizado.html", total=total)


@app.route("/vendas")
def vendas():
    lista_vendas = listar_vendas()

    quantidade = len(lista_vendas)
    total = sum((Decimal(str(v["total"])) for v in lista_vendas), Decimal("0"))

    return render_template(
        "vendas.html",
        vendas=lista_vendas,
        quantidade=quantidade,
        total=total,
    )


@app.route("/encerrar")
def encerrar():
    # Esta rota encerra o caixa da aplicação.
    # Os produtos permanecem no MySQL; somente o carrinho atual é limpo.
    session["carrinho"] = []
    return render_template("encerrar.html")


if __name__ == "__main__":
    app.run(debug=True)
