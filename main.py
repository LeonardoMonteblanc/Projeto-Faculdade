from flask import Flask, request, redirect, render_template, url_for, send_file
import csv
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def index():
    return render_template('index.html', methods=['GET'])


@app.route("/aluno", methods =["GET", "POST"])
def aluno():
    if request.method == 'POST':
        nome = request.form.get('nome-completo')
        telefone = request.form.get('telefone')
        nome_pai = request.form.get('nome-pai')
        nome_mae = request.form.get('nome-mae')

        with open ('db.csv', mode='a') as db_file:
            db_file = csv.writer(db_file, delimiter=';')
            db_file.writerow([nome, telefone, nome_pai, nome_mae])
    
    return render_template('aluno.html', retorno='As informações foram gravadas com sucesso no banco!')


@app.route("/pagamento", methods =["GET", "POST"])
def pagamento():
    f = open('./db.csv')
    if request.method == 'POST':
        if request.form['submit-button'] == "Submit":

            for checkbox in request.form.getlist('check'):
                
                file = csv.reader(f, delimiter=";")
                lista = list(file)

                for i in lista:
                    print(i)
                    print(checkbox)
                    if str(i) == str(checkbox):
                        lista.remove(i)

                with open("db.csv", mode="w") as f:
                    f = csv.writer(f, delimiter=";")

                    for i in lista:
                        f.writerow(i)

    
    with open('db.csv') as other_file:
        reader = csv.reader(other_file,  delimiter=';')
        return render_template('pagamento.html', csv=reader)

@app.route("/download")
def download():
    return send_file(
            'db.csv',
            mimetype='text/csv',
            download_name='Pendencias.csv',
            as_attachment=True
        )
@app.route('/upload')
def upload():
    return render_template('upload.html', methods=['GET'])


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      extensao = f.filename.split('.')[-1]

    if extensao == 'csv':
        # se já existir o arquivo com esse nome, invés de substituir os dados, só adicionar ao arquivo
        f.filename = 'db.csv'
        f.save(secure_filename(f.filename))
        return render_template('upload.html', methods=['GET'], sucess='Upload realizado com sucesso!!')
    else:
        return render_template('upload.html', methods=['GET'], sucess='Arquivo não é csv!')

if __name__ == "__main__":
    app.run()
