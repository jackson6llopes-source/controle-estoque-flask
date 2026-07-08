from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
url = os.environ.get('DATABASE_URL')

if url:
    url = url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = url or 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 🔹 MODELO DO BANCO
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    t34 = db.Column(db.Integer, default=0)
    t35 = db.Column(db.Integer, default=0)
    t36 = db.Column(db.Integer, default=0)
    t37 = db.Column(db.Integer, default=0)
    t38 = db.Column(db.Integer, default=0)
    t39 = db.Column(db.Integer, default=0)


@app.route('/')
def index():
    return render_template('index.html')


# 🔹 CADASTRAR
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        sku = request.form['sku'].strip().upper()

        produto = {}
        for i in range(34, 40):
            produto[str(i)] = int(request.form[str(i)])

        produto_existente = Produto.query.filter_by(sku=sku).first()

        if produto_existente:
            produto_existente.t34 += produto['34']
            produto_existente.t35 += produto['35']
            produto_existente.t36 += produto['36']
            produto_existente.t37 += produto['37']
            produto_existente.t38 += produto['38']
            produto_existente.t39 += produto['39']
        else:
            novo_produto = Produto(
                sku=sku,
                t34=produto['34'],
                t35=produto['35'],
                t36=produto['36'],
                t37=produto['37'],
                t38=produto['38'],
                t39=produto['39']
            )
            db.session.add(novo_produto)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('cadastrar.html')


# 🔹 VER ESTOQUE
@app.route('/ver_reposicoes')
def ver_reposicoes():
    produtos = Produto.query.all()
    return render_template('ver_reposicoes.html', reposicao=produtos)


# 🔹 PESQUISAR
@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    resultados = []

    if request.method == 'POST':
        termo = request.form['sku'].upper()
        resultados = Produto.query.filter(Produto.sku.contains(termo)).all()

    return render_template('pesquisar.html', resultados=resultados)


# 🔹 REMOVER
@app.route('/remover', methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        sku = request.form['sku'].strip().upper()

        produto = Produto.query.filter_by(sku=sku).first()

        if produto:
            for i in range(34, 40):
                tamanho = f"t{i}"
                remover_qtd = int(request.form[str(i)])

                valor_atual = getattr(produto, tamanho)

                if valor_atual >= remover_qtd:
                    setattr(produto, tamanho, valor_atual - remover_qtd)
                else:
                    setattr(produto, tamanho, 0)

            # 🔥 remove produto se tudo for zero
            if all(getattr(produto, f"t{i}") == 0 for i in range(34, 40)):
                db.session.delete(produto)

            db.session.commit()

        return redirect(url_for('index'))

    return render_template('remover.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)