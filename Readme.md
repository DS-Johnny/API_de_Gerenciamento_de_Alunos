# API de Gerenciamento de Alunos

## Descrição
Esta é uma API REST desenvolvida em Flask para gerenciamento de alunos. Ela permite realizar operações CRUD (Create, Read, Update e Delete) em um banco de dados SQLite.

## Tecnologias Utilizadas
- Python 3
- Flask
- SQLite

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/DS-Johnny/API_de_Gerenciamento_de_Alunos.git
   cd seu-repositorio
   ```
2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/macOS
   venv\Scripts\activate  # Para Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração do Banco de Dados
Certifique-se de ter um banco de dados SQLite configurado corretamente. A conexão é gerenciada pelo arquivo `database.py`, que contém uma função `get_db()` para abrir a conexão com o banco.

## Executando a API

Para iniciar o servidor Flask, execute:
```bash
python app.py
```

O servidor será iniciado em `http://127.0.0.1:5000/`.

## Autenticação
A API requer autenticação básica via HTTP (Basic Auth). As credenciais padrões são:
- **Usuário**: `admin`
- **Senha**: `password`

## Endpoints

### 1. Listar todos os alunos
**GET** `/aluno`

**Resposta:**
```json
{
  "Alunos": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com",
      "curso": "Ciência da Computação",
      "ano": 2024
    }
  ]
}
```

### 2. Buscar aluno por ID
**GET** `/aluno/<id>`

**Resposta:**
```json
{
  "Aluno": {
    "ID": 1,
    "Nome": "João Silva",
    "Curso": "Ciência da Computação",
    "Ano": 2024
  }
}
```

### 3. Adicionar um novo aluno
**POST** `/aluno`

**Corpo da Requisição:**
```json
{
  "nome": "Maria Oliveira",
  "email": "maria@email.com",
  "curso": "Engenharia",
  "ano": 2025
}
```

**Resposta:**
```json
{
  "id": 2,
  "nome": "Maria Oliveira",
  "email": "maria@email.com",
  "curso": "Engenharia",
  "ano": 2025
}
```

### 4. Atualizar dados de um aluno
**PUT/PATCH** `/aluno/<id>`

**Corpo da Requisição:**
```json
{
  "nome": "Maria Oliveira",
  "email": "maria.oliveira@email.com",
  "curso": "Engenharia Civil",
  "ano": 2025
}
```

**Resposta:**
```json
{
  "id": 2,
  "nome": "Maria Oliveira",
  "email": "maria.oliveira@email.com",
  "curso": "Engenharia Civil",
  "ano": 2025
}
```

### 5. Remover um aluno
**DELETE** `/aluno/<id>`

**Resposta:**
```json
{
  "Alerta": "O aluno foi removido do banco de dados."
}
```


