from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        # Padroniza o SKU (evita duplicidade tipo "a123" e "A123 ")
        sku = request.form['sku'].strip().upper()

        produto = {'SKU': sku}

        for i in range(34, 40):
            produto[str(i)] = int(request.form[str(i)])

        # Carrega JSON com segurança
        if os.path.exists('estoque.json'):
            try:
                with open('estoque.json', 'r') as f:
                    reposicao = json.load(f)
            except:
                reposicao = []
        else:
            reposicao = []

        # Controle para saber se encontrou o SKU
        sku_encontrado = False

        for item in reposicao:
            # Padroniza também o SKU do JSON
            if item['SKU'].strip().upper() == sku:
                for i in range(34, 40):
                    item[str(i)] += produto[str(i)]
                sku_encontrado = True
                break

        # Só adiciona se NÃO existir
        if not sku_encontrado:
            reposicao.append(produto)

        # Salva o JSON atualizado
        with open('estoque.json', 'w') as f:
            json.dump(reposicao, f, indent=4)

        return redirect(url_for('index'))

    return render_template('cadastrar.html')


@app.route('/ver_reposicoes',)
def ver_reposicoes():
    if os.path.exists('estoque.json'):
        with open('estoque.json', 'r') as f:
            reposicao = json.load(f)
            # Garantir que as chaves são strings
            for item in reposicao:
                # Cria um novo dicionário com chaves como strings
                item_str = {}
                for i in range(34, 40):
                    item_str[str(i)] = item[str(i)]
                item['SKU'] = item['SKU']
                item.update(item_str)
    else:
        reposicao = []

    return render_template('ver_reposicoes.html', reposicao=reposicao)

@app.route('/pesquisar', methods=['GET', 'POST'])
def pesquisar():
    resultados = []

    if request.method == 'POST':
        termo = request.form['sku'].lower()

        if os.path.exists('estoque.json'):
            with open('estoque.json', 'r') as f:
                reposicao = json.load(f)

                # Filtra os SKUs que contêm o termo digitado
                for item in reposicao:
                    if termo in item['SKU'].lower():
                        resultados.append(item)

    return render_template('pesquisar.html', resultados=resultados)

@app.route('/remover', methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        sku = request.form['sku'].strip().upper()

        # Quantidades que serão removidas
        remover_qtd = {}
        for i in range(34, 40):
            remover_qtd[str(i)] = int(request.form[str(i)])

        # Carrega o JSON
        if os.path.exists('estoque.json'):
            try:
                with open('estoque.json', 'r') as f:
                    reposicao = json.load(f)
            except:
                reposicao = []
        else:
            reposicao = []

        for item in reposicao:
            if item['SKU'].strip().upper() == sku:

                # Remove as quantidades
                for i in range(34, 40):
                    tamanho = str(i)

                    if item[tamanho] >= remover_qtd[tamanho]:
                        item[tamanho] -= remover_qtd[tamanho]
                    else:
                        item[tamanho] = 0

                break

        # 🔥 Remove o SKU se todos os tamanhos forem zero
        reposicao = [
            item for item in reposicao
            if any(item[str(i)] > 0 for i in range(34, 40))
        ]

        # Salva o JSON atualizado
        with open('estoque.json', 'w') as f:
            json.dump(reposicao, f, indent=4)

        return redirect(url_for('index'))

    return render_template('remover.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)