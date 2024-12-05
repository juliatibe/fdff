from flask import Flask, render_template,  request, flash, url_for, redirect
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ua_chave_secreta_aqui'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO (2)\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)


class Cadastro:
    def __int__(self, id_cadastro, nome, email, senha):
        self.id_cadastro = id_cadastro
        self.nome = nome
        self.email = email
        self.senha = senha

class Agendamento:
    def __int__(self, id_agendamento, nome, email, telefone, horario, observacoes):
        self.id_agendamento = id_agendamento
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.horario = horario
        self.observacoes = observacoes

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/abrir_agendamento')
def agendamento():
    return render_template('agendamento.html')

@app.route('/criar_agendamento', methods=['POST'])
def criar_agendamento():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    horario = request.form['horario']
    observacoes = request.form['observacoes']

    cursor = con.cursor()

    cursor.execute("INSERT INTO AGENDAMENTO (NOME, EMAIL, TELEFONE, HORARIO, OBSERVACOES) VALUES(?, ?, ?, ?, ?)",
                   (nome, email, telefone, horario, observacoes))
    con.commit()

    flash("Consulta cadastrada com sucesso!", "success")
    return render_template('agendamento.html')


@app.route('/abrir_cadastro')
def abrir_cadastro():
    return render_template('cadastro.html')

@app.route('/editar')
def editar():
    # recupera paramentro get
    id = request.args.get('id')

    cursor = con.cursor()
    cursor.execute('SELECT * FROM agendamento WHERE id_agendamento = ?', (id, ))
    agendamento = cursor.fetchone()
    cursor.close()

    print(id)

    return render_template('editar.html', agendamento=agendamento)


@app.route('/editar_agendamento', methods=['POST'])
def editarAgendamento():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    horario = request.form['horario']
    observacoes = request.form['observacoes']

    cursor = con.cursor()
    cursor.execute("UPDATE agendamentos SET NOME = ?, EMAIL = ?, TELEFONE = ?, HORARIO = ?, OBSERVACOES = ? WHERE ID_AGENDAMENTO = ?",
                   (nome, email, telefone, horario, observacoes, id))

    con.commit()

    cursor.close()
    flash("Agendamento atualizado com sucesso!", "success")
    return redirect(url_for('veterinario'))  # Redireciona para a página principal após a atualização



    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se o livro já existe
        cursor.execute("SELECT * FROM CADASTRO WHERE EMAIL = ?", (email,))
        if cursor.fetchone():
            flash("Erro: Email e Senha já cadastrado.", "error")
            return redirect(url_for('abrir_cadastro'))

        # Inserir o novo livro (sem capturar o ID)
        cursor.execute("INSERT INTO CADASTRO (NOME, EMAIL, SENHA) VALUES(?, ?, ?)",
                       (name, email, password))
        con.commit()
    finally:
        # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()

    flash("Veterinário cadastrado com sucesso!", "success")
    return redirect(url_for('abrir_cadastro'))



@app.route('/cadastro')
def cadastro():
    cursor = con.cursor()
    cursor.execute('SELECT id_cadastro, nome, email, senha FROM cadastro')
    cadastro = cursor.fetchall()
    cursor.close()
    return render_template('cadastro.html', cadastro=cadastro)


@app.route('/veterinario', methods=['POST'])
def veterinario():
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()
    cursor.execute('SELECT * FROM cadastro where email = ? AND senha = ?', (email, senha))
    usuario = cursor.fetchone()

    if usuario is None:
        return render_template('cadastro.html')

    cursor.close()

    cursor = con.cursor()
    cursor.execute('SELECT * FROM agendamento', ())
    agendamentos = cursor.fetchall()



    return render_template('veterinario.html', agendamentos=agendamentos)


if __name__ == '__main__':
    app.run(debug=True)

