from flask import Flask, render_template, request, redirect
import os
from PDF_Reader_Patterns import LicitacaoReader
import sqlite3

app = Flask(__name__)

# Configurações gerais
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Conexão SQLite
def get_db_connection():
    conn = sqlite3.connect("hanashiro.db")
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn

# Página inicial
@app.route('/')
def index():
    return render_template('index.html', active_page='home')

# Listar fornecedores
@app.route('/fornecedores')
def listar_fornecedores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedor")
    fornecedores = cursor.fetchall()
    conn.close()
    return render_template('fornecedores.html', fornecedores=fornecedores, active_page='fornecedores')

# Cadastrar novo fornecedor
@app.route('/fornecedores/novo', methods=['GET', 'POST'])
def novo_fornecedor():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        contato = request.form['contato']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fornecedor (nome, cnpj, email, telefone, endereco, contato_responsavel)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, cnpj, email, telefone, endereco, contato))
        conn.commit()
        conn.close()
        return redirect('/fornecedores')

    return render_template('novo_fornecedor.html', active_page='fornecedores/novo')

# Upload e leitura de PDF
@app.route('/upload', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        pdf = request.files.get('pdf')

        if not pdf or not pdf.filename.endswith('.pdf'):
            return "Envie um arquivo PDF válido!"

        path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
        pdf.save(path)

        leitor = LicitacaoReader(path)
        resultados = leitor.process_edital()

        return render_template('resultado.html', resultados=resultados, active_page='upload')

    return render_template('upload.html', active_page='upload')


if __name__ == '__main__':
    app.run(debug=True)
