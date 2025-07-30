## Como rodar o projeto

Siga os passos abaixo para configurar e executar o projeto corretamente.
1. Clonar o repositório

git clone https://github.com/RafaelAnanias/projetoBancoDados.git
cd projetoBancoDados

2. Criar e ativar o ambiente virtual
py -3 -m venv .venv
.venv\Scripts\activate

3. Instalar as dependências
pip install -r requirements.txt

4. Configurar o banco de dados no XAMPP
5. Abra o XAMPP e inicie o MySQL.
6. Acesse o phpMyAdmin.
7. Crie o banco de dados com o seguinte comando: CREATE DATABASE db_nomeDoSeuBanco;
8. Importe o arquivo SQL enviado com este projeto para popular o banco.

9. Configurar o arquivo .env
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

DATABASE_URI = 'mysql://root:@localhost/db_nomeDoSeuBanco'
SECRET_KEY = 'SuaSenhaSecreta'

Substitua SuaSenhaSecreta por uma chave segura de sua escolha.

10. Executar o projeto
flask --app main.py run --debug
