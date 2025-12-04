import requests
from flask import Flask, request, render_template

# Indica ao Flask o modulo principal, onde tem os arquivos CSS e HTML
app = Flask(__name__, static_url_path='/static')

# Rota, direciona para pagina html principal
@app.route('/', methods=['GET'])
def index():
    return render_template('cep.html')

# Rota, recebe valores GET e POST
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    # aceita somente valores POST
    if request.method == 'POST':
        cep = request.form['cep']
        # Removendo ponto, virgula e espaços em brancos, evita erro 
        cep = cep.replace(".", "").replace("-", "").replace(" ", "")
        # verificando se tem 8 Digitos, padrão de ceps no brasil
        if len(cep) == 8:
            try:
                link = f"https://viacep.com.br/ws/{cep}/json"
                requisicao = requests.get(link, verify=False)
                lista = requisicao.json()
                rua = lista['logradouro']
                bairro = lista['bairro']
                localidade = lista['localidade'] +'/'+ lista['uf']
                # passando os valores obtidos para pagina HTML.
                return render_template('consulta.html', rua=rua, bairro=bairro, localidade=localidade, cep=cep)

            except:
                return render_template('cep.html', aviso='Cep não existe !')

        else:
            return render_template('cep.html', aviso="Cep Invalido")

    else:
        # Direcionado para pagina principal
        return render_template('cep.html')
    
if __name__ == '__main__':
    app.run()


