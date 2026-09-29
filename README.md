# RHIZEL - Loja de Roupas

Projeto desenvolvido para criar uma aplicação web simples de uma loja de roupas, permitindo cadastrar produtos, adicionar fotos, selecionar tamanhos, adicionar produtos ao carrinho e registrar vendas.

O projeto também foi desenvolvido com o objetivo de praticar conceitos de desenvolvimento web, integração com banco de dados e organização de uma aplicação Python.

## Funcionalidades

- Cadastro de produtos
- Cadastro de preço e descrição
- Upload de até 3 fotos por produto
- Cadastro de tamanhos disponíveis
- Visualização dos produtos
- Página de detalhes do produto
- Carrinho de compras
- Finalização de vendas
- Relatório de vendas
- Armazenamento dos dados no MySQL

## Tecnologias utilizadas

### Backend

- Python
- Flask
- MySQL
- mysql-connector-python

### Frontend

- HTML5
- CSS3
- JavaScript

### Outras ferramentas

- MySQL Workbench
- Git
- GitHub
- Python Virtual Environment (venv)

## Banco de dados

O projeto utiliza o MySQL para armazenar as informações da loja.

O banco possui as seguintes tabelas:

- `produtos` — informações dos produtos
- `imagens_produto` — caminhos das imagens dos produtos
- `produto_tamanhos` — tamanhos disponíveis
- `vendas` — vendas realizadas
- `itens_venda` — produtos pertencentes a cada venda

As tabelas possuem relacionamentos através de chaves estrangeiras.

## Upload de imagens

As imagens dos produtos são selecionadas diretamente do computador através do formulário de cadastro.

As imagens são armazenadas na pasta:

```text
static/imagens/
```
![Texto alternativo da imagem](./Captura de tela 2026-09-29 184037.png)
