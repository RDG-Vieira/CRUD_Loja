import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crud', 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'sua_chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email=? AND senha=?', (email, senha))
        usuario = cursor.fetchone()
        if usuario:
            conn.close()
            return redirect(url_for('pagina_formulario'))
        else:

            try:
                cursor.execute('INSERT INTO usuarios (email, senha) VALUES (?, ?)', (email, senha))
                conn.commit()
                conn.close()
                return redirect(url_for('pagina_formulario'))
            except sqlite3.IntegrityError:
                conn.close()
                flash('Erro ao criar usuário.')
                return redirect(url_for('login'))
    return render_template('login.html')

client = MongoClient('mongodb://localhost:27017/')
db = client['crud']  # Banco de dados 'crud'
colecao_vendas = db['vendas']  # Collection 'vendas'

@app.route('/cadastrar_vendas', methods=['GET', 'POST'])
def cadastrar_vendas():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        codigo = request.form['codigo']
        data = request.form['data']
        observacao = request.form['observacao']

        venda = {
            'nome': nome,
            'valor': float(valor.replace('R$', '').replace('.', '').replace(',', '.')),
            'codigo': codigo,
            'data': data,
            'observacao': observacao
        }
        colecao_vendas.insert_one(venda)
        flash('Venda cadastrada com sucesso!')
        return redirect(url_for('cadastrar_vendas'))

    # Busca apenas os 5 últimos cadastrados
    vendas = list(colecao_vendas.find().sort('_id', -1).limit(5))
    return render_template('cadastrar_vendas.html', vendas=vendas)

@app.route('/cadastrar_clientes', methods=['GET', 'POST'])
def cadastrar_clientes():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        observacao = request.form['observacao']

        cliente = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'endereco': endereco,
            'observacao': observacao
        }
        db['clientes'].insert_one(cliente)
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('cadastrar_clientes'))  # <-- redireciona para a página de clientes

    clientes = list(db['clientes'].find().sort('_id', -1).limit(5)) 
    return render_template('cadastrar_clientes.html', clientes=clientes)

@app.route('/excluir_cliente/<id>', methods=['POST'])
def excluir_cliente(id):
    db['clientes'].delete_one({'_id': ObjectId(id)})
    flash('Cliente excluído com sucesso!')
    return redirect(url_for('cadastrar_clientes'))  # <-- redireciona para a página de clientes

@app.route('/atualizar_cliente/<id>', methods=['GET', 'POST'])
def atualizar_cliente(id):
    cliente = db['clientes'].find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        observacao = request.form['observacao']
        db['clientes'].update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'endereco': endereco,
                'observacao': observacao
            }}
        )
        flash('Cliente atualizado com sucesso!')
        return redirect(url_for('cadastrar_clientes'))  # <-- redireciona para a página de clientes
    return render_template('atualizar_cliente.html', cliente=cliente)

@app.route('/pagina_formulario')
def pagina_formulario():
    return render_template('pagina_formulario.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/politica_tratamento_dados')
def politica_tratamento_dados():
    return render_template('politica_tratamentodados.html')

@app.route('/excluir_venda/<id>', methods=['POST'])
def excluir_venda(id):
    colecao_vendas.delete_one({'_id': ObjectId(id)})
    flash('Venda excluída com sucesso!')
    return redirect(url_for('cadastrar_vendas'))

@app.route('/atualizar_venda/<id>', methods=['GET', 'POST'])
def atualizar_venda(id):
    venda = colecao_vendas.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nome = request.form['nome']
        valor = float(request.form['valor'].replace('R$', '').replace('.', '').replace(',', '.'))
        codigo = request.form['codigo']
        data = request.form['data']
        observacao = request.form['observacao']
        colecao_vendas.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'nome': nome,
                'valor': valor,
                'codigo': codigo,
                'data': data,
                'observacao': observacao
            }}
        )
        flash('Venda atualizada com sucesso!')
        return redirect(url_for('cadastrar_vendas'))
    return render_template('atualizar_venda.html', venda=venda)

@app.route('/baixar_vendas_pdf', methods=['POST'])
def baixar_vendas_pdf():
    data_inicio = request.form.get('data_inicio')
    data_fim = request.form.get('data_fim')

    filtro = {}
    if data_inicio and data_fim:
        filtro['data'] = {'$gte': data_inicio, '$lte': data_fim}
    elif data_inicio:
        filtro['data'] = {'$gte': data_inicio}
    elif data_fim:
        filtro['data'] = {'$lte': data_fim}

    vendas = list(colecao_vendas.find(filtro))

    output = io.BytesIO()
    p = canvas.Canvas(output, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, height - 40, "Relatório de Vendas")

    p.setFont("Helvetica-Bold", 10)
    y = height - 70
    p.drawString(40, y, "Nome")
    p.drawString(170, y, "Valor")
    p.drawString(240, y, "Código")
    p.drawString(320, y, "Data")
    p.drawString(400, y, "Observação")

    p.setFont("Helvetica", 10)
    y -= 20
    for venda in vendas:
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(40, y, str(venda.get('nome', '')))
        p.drawString(170, y, "R$ {:.2f}".format(float(venda.get('valor', 0))))
        p.drawString(240, y, str(venda.get('codigo', '')))
        p.drawString(320, y, str(venda.get('data', '')))
        p.drawString(400, y, str(venda.get('observacao', '')))
        y -= 18

    p.save()
    output.seek(0)

    return send_file(
        output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='vendas.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)