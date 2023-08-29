import requests
from flask import Flask, request, jsonify, render_template

# Static pasta de CSS
app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def index():
    return render_template('cep.html')


@app.errorhandler(404)  # Tratamento de erro
def erro_page(error):
    return render_template('cep.html', aviso='Pagina Não Existe !'), 404


@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':  # Validando requisição POST e GET impede erro ao acessar direto.
        cep = request.form['cep']
        cep = cep.replace(".", "").replace("-", "").replace(" ", "")  # formatando valor recebido
        if len(cep) == 8:  # validando quantidade de digitos
            try:
                link = f"https://viacep.com.br/ws/{cep}/json"
                requisicao = requests.get(link, verify=False)
                lista = requisicao.json()
                ceps = lista['cep']
                rua = lista['logradouro']
                compl = lista['complemento']
                bairro = lista['bairro']
                localidade = lista['localidade'] +'/'+ lista['uf']

            except:
                erro = f'Cep não existe !'
                return render_template('cep.html', aviso=erro)

            return render_template('consulta.html', rua=rua , bairro=bairro, localidade=localidade , cep=cep)

        else:
            erro =  "Verifique os Digitos"
            return render_template('cep.html', aviso=erro)

    else:
        return render_template('cep.html')

if __name__ == '__main__':
    app.run()
