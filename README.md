Documentação do Sistema CRUD RDG-Data Science
Objetivo do Projeto
Este projeto foi criado com o objetivo de ajudar a empresa onde faço estágio.
Atualmente, a empresa não possui um sistema digital, o que torna os processos mais
lentos e manuais. Com esse sistema, conseguimos tornar as atividades mais rápidas
e organizadas, automatizando boa parte das tarefas do dia a dia.
Preparando o Ambiente (somente para Windows)
Antes de começar a usar o sistema, é necessário configurar o ambiente virtual, que
ajuda a manter as ferramentas organizadas. Passo a passo:
1. Abra o terminal (Prompt de Comando ou PowerShell) na pasta onde está o
projeto.
2. Crie o ambiente virtual com:
 python -m venv .venv
3. Ative o ambiente com:
 .\.venv\Scripts\activate
4. Instale as bibliotecas necessárias com:
 pip install flask pymongo reportlab
5. Para sair do ambiente, use:
 deactivate
6. Sempre que for trabalhar no projeto, ative novamente com:
 .\.venv\Scripts\activate
Bibliotecas Utilizadas
Estas são as bibliotecas usadas no projeto:
- os
- sqlite3
- io
- flask
- pymongo
- bson (vem com pymongo)
- reportlab
As bibliotecas 'os', 'sqlite3' e 'io' já vêm com o Python.
As outras devem ser instaladas com o comando:
 pip install flask pymongo reportlab
Como Iniciar o Sistema
1. Execute o arquivo models.py (ele configura o banco de dados SQLite). Que irá
salvar os logins e senha dos usuários.
2. Abra o arquivo backend.py no VS Code.
3. Execute o backend.py e aguarde aparecer a mensagem:
 Running on http://127.0.0.1:5000
4. Pressione Ctrl e clique no link para abrir o sistema no navegador.
Tela de Login (Atualizada)
Assim que o sistema é iniciado, a primeira tela que aparece é a de login.
O sistema faz autenticação real dos usuários. Isso significa que:
- É obrigatório usar um e-mail válido (ex: emaildeexemplo@gmail.com).
- O e-mail e a senha são salvos em um banco de dados SQLite.
- Não é possível cadastrar o mesmo e-mail com outra senha.
- Por isso, é importante lembrar os dados utilizados no cadastro.
Funcionamento do Sistema
Depois de fazer login com sucesso, você será redirecionado para a página inicial.
Nela, é possível escolher o tipo de serviço desejado: Cadastro de Cliente ou Cadastro
de Venda.
Se escolher cadastrar um cliente, você verá um formulário com os seguintes campos:
- Nome (obrigatório)
- CPF (obrigatório)
- CEP (obrigatório)
- Endereço (obrigatório)
- Número de telefone
- Sexo
- E-mail
Esses dados são armazenados em conformidade com a LGPD e podem ser mantidos
por até 2 anos.
Como Ver os Usuários Salvos
Para verificar os usuários registrados no banco de dados:
1. Abra o terminal (Prompt de Comando ou PowerShell).
2. Vá até a pasta onde está o arquivo ver_usuarios.py. Exemplo:
 cd "C:\Users\faiel\OneDrive\Área de Trabalho\aulaterca"
3. Execute o comando:
 python ver_usuarios.py