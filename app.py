from flask import Flask, g, request, jsonify
from database import get_db
from functools import wraps

app = Flask(__name__)


# ---------------------------------- Autenticação
# Definição das credenciais para autenticação básica
api_username = 'admin'
api_password = 'password'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization  # Obtém as credenciais enviadas na requisição
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)  # Se as credenciais estiverem corretas, executa a função
        else:
            return jsonify({'Alerta' : 'Autenticação Falhou!'}), 403  # Caso contrário, retorna erro 403
    return decorated

# ---------------------------------- Banco de dados
@app.teardown_appcontext
# Fecha a conexão com o banco de dados SQLite ao final de cada requisição
# Isso evita que conexões fiquem abertas desnecessariamente
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ----------------------------------- Rotas
@app.route('/aluno', methods=['GET'])
@protected  # Protege a rota com autenticação
def get_alunos():
    db = get_db()
    cursor = db.execute('SELECT * FROM alunos')  # Consulta todos os alunos na tabela
    result = cursor.fetchall()

    alunos = []  # Lista para armazenar os alunos
    for aluno in result:
        aluno_dict = {}
        aluno_dict['id'] = aluno['id']
        aluno_dict['nome'] = aluno['nome']
        aluno_dict['email'] = aluno['email']
        aluno_dict['curso'] = aluno['curso']
        aluno_dict['ano'] = aluno['ano']
        alunos.append(aluno_dict)
    
    return jsonify({'Alunos' : alunos})  # Retorna a lista de alunos no formato JSON

@app.route('/aluno/<int:aluno_id>', methods=['GET'])
@protected  # Protege a rota com autenticação
def get_aluno(aluno_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM alunos WHERE id = ?', [aluno_id])  # Busca um aluno pelo ID
    result = cursor.fetchone()
    return jsonify({'Aluno' : {"ID" : result['id'], 
                               "Nome" : result['nome'], 
                               "Curso" : result['curso'], 
                               "Ano" : result['ano']}})  # Retorna o aluno encontrado

@app.route('/aluno', methods=['POST'])
@protected  # Protege a rota com autenticação
# Adiciona um novo aluno ao banco de dados
def add_aluno():
    novo_aluno = request.get_json()  # Obtém os dados do novo aluno a partir do JSON enviado na requisição
    nome = novo_aluno['nome']
    email = novo_aluno['email']
    curso = novo_aluno['curso']
    ano = novo_aluno['ano']

    db = get_db()
    db.execute('INSERT INTO alunos (nome, email, curso, ano) values (?,?,?,?)', [nome,email,curso,ano])
    db.commit()  # Salva a alteração no banco

    # Obtém o aluno recém-adicionado para retornar na resposta
    cursor = db.execute('SELECT id, nome, email, curso, ano FROM alunos WHERE nome = ?', [nome])
    result = cursor.fetchone()

    return jsonify({"id" : result['id'], 
                    "nome" : result['nome'], 
                    "email" : result['email'], 
                    "curso" : result['curso'],
                    "ano" : result['ano']})

@app.route('/aluno/<int:aluno_id>', methods=['PUT', 'PATCH'])
@protected  # Protege a rota com autenticação
# Edita os dados de um aluno existente
def edit_aluno(aluno_id):
    aluno_info = request.get_json()  # Obtém os novos dados do aluno a partir do JSON enviado
    nome = aluno_info['nome']
    email = aluno_info['email']
    curso = aluno_info['curso']
    ano = aluno_info['ano']

    db = get_db()
    db.execute('UPDATE alunos SET nome = ?, email = ?, curso = ?, ano = ? WHERE id = ?', [nome, email, curso, ano, aluno_id])
    db.commit()  # Salva a alteração no banco

    # Obtém o aluno atualizado para retornar na resposta
    cursor = db.execute('SELECT id, nome, email, curso, ano FROM alunos WHERE id = ?', [aluno_id])
    result = cursor.fetchone()

    return jsonify({"id" : result['id'], 
                    "nome" : result['nome'], 
                    "email" : result['email'], 
                    "curso" : result['curso'],
                    "ano" : result['ano']})

@app.route('/aluno/<int:aluno_id>', methods=['DELETE'])
@protected  # Protege a rota com autenticação
# Deleta um aluno do banco de dados
def delete_aluno(aluno_id):
    db = get_db()
    db.execute('DELETE FROM alunos WHERE id = ?', [aluno_id])  # Remove o aluno pelo ID
    db.commit()  # Salva a alteração no banco

    return jsonify({"Alerta" : "O aluno foi removido do banco de dados."})

if __name__ == '__main__':
    app.run(debug=True)
