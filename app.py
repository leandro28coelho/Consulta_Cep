import requests
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def index():
    return render_template('cep.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        cep = request.form['cep']
        cep = cep.replace(".", "").replace("-", "").replace(" ", "")
        if len(cep) == 8:
            try:
                link = f"https://viacep.com.br/ws/{cep}/json"
                requisicao = requests.get(link, verify=False)
                lista = requisicao.json()
                rua = lista['logradouro']
                bairro = lista['bairro']
                localidade = lista['localidade'] +'/'+ lista['uf']
                return render_template('consulta.html', rua=rua, bairro=bairro, localidade=localidade, cep=cep)

            except:
                return render_template('cep.html', aviso='Cep não existe !')

        else:
            return render_template('cep.html', aviso="Verifique os Digitos")

    else:
        return render_template('cep.html')

if __name__ == '__main__':
    app.run()


# 
