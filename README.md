# RHIZEL Loja — Flask + MySQL

Projeto de estudo de uma loja de roupas com:

- Python + Flask
- HTML + CSS + JavaScript
- MySQL
- Cadastro de produtos
- Upload de até 3 fotos pelo computador
- Tamanhos P, M, G, GG e XG
- Carrinho
- Finalização de venda
- Relatório de vendas
- Banco de dados relacional

## 1. O que você precisa instalar

Tenha instalado:

1. Python
2. MySQL Server
3. MySQL Workbench

## 2. Criar o banco

Abra o MySQL Workbench.

Abra o arquivo `database.sql` deste projeto, copie todo o conteúdo para uma nova aba SQL e execute.

Depois confira:

```sql
USE rhizel_loja;
SHOW TABLES;
```

Você deverá encontrar:

- produtos
- imagens_produto
- produto_tamanhos
- vendas
- itens_venda

## 3. Criar o ambiente virtual

No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv venv
```

Ative:

```powershell
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, você pode executar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

e depois:

```powershell
.\venv\Scripts\Activate.ps1
```

## 4. Instalar as bibliotecas

```powershell
pip install -r requirements.txt
```

## 5. Configurar o MySQL

Faça uma cópia de `.env.example` e renomeie a cópia para:

```text
.env
```

Abra `.env` e coloque sua senha do MySQL:

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=SUA_SENHA
MYSQL_DATABASE=rhizel_loja
```

Não compartilhe o arquivo `.env`. Ele já está no `.gitignore`.

## 6. Executar o projeto

Com o ambiente virtual ativado:

```powershell
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

## 7. Como o cadastro de fotos funciona

Na tela de cadastro, agora você não precisa colocar URL.

Você poderá selecionar:

- Foto 1
- Foto 2
- Foto 3

As fotos serão copiadas para:

```text
static/imagens/
```

O MySQL não guarda a imagem diretamente. Ele guarda o caminho da imagem.

Exemplo:

```text
imagens/8b3c2f1a9c1a4e0c8d4c0b6d8e8d7a11.jpg
```

Isso deixa o projeto mais simples para aprender e permite futuramente trocar o armazenamento local por um serviço de arquivos/nuvem.

## 8. Estrutura do projeto

```text
projeto_loja_rhizel_mysql/
│
├── app.py
├── banco.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── produto.html
│   ├── cadastrar.html
│   ├── relatorio.html
│   ├── vendas.html
│   ├── finalizado.html
│   └── encerrar.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── imagens/
```

## 9. Fluxo do sistema

```text
Navegador
   ↓
Flask (app.py)
   ↓
banco.py
   ↓
MySQL
```

Para imagens:

```text
Computador
   ↓
Flask
   ↓
static/imagens/
```

E o MySQL guarda apenas o caminho:

```text
produto
   └── imagem → "imagens/foto.jpg"
```

## 10. Primeira execução recomendada

1. Criar o banco pelo `database.sql`.
2. Conferir `SHOW TABLES;`.
3. Criar o ambiente virtual.
4. Instalar `requirements.txt`.
5. Criar `.env`.
6. Rodar `python app.py`.
7. Abrir `http://127.0.0.1:5000`.
8. Cadastrar um produto.
9. Selecionar uma foto do computador.
10. Conferir a foto em `static/imagens/`.
11. Conferir os dados no MySQL.

