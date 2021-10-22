from flask import Flask, render_template, request, flash
from markupsafe import escape
from db import accion, seleccion
from werkzeug.security import generate_password_hash
from os import urandom

web = Flask(__name__)
web.secret_key = urandom(24)

@web.errorhandler(404)
def error404(e) -> tuple:
    """ Se encarga de gestionar el error """
    return render_template('404.html'), 404

@web.route('/')
@web.route('/home/')
@web.route('/index/')
def index():
    return render_template('index.html')

@web.route('/grabar/')
def mostrarformgrabar():
    return render_template('grabar.html')

@web.route('/grabar/', methods=['POST'])
def recibirformgrabar():
    # 1. Recuperar los datos del formulario
    usr = escape(request.form['txtusr'].strip())
    pwd = escape(request.form['txtpwd'].strip())
    # 2. Validar los datos
    validos = True
    if usr==None or len(usr)==0:
        flash("El usuario es requerido")
        validos = False
    if pwd==None or len(pwd)==0:
        flash("La clave es requerida")
        validos = False
    # 3. Grabar sobre la base de datos
    if validos:
        # a) Escribir la consulta (Consulta parametrica)
        #sql = f"INSERT INTO tablita(login, clave) VALUES ('{usr}', '{pwd}')"
        sql = 'INSERT INTO tablita(login, clave) VALUES (?, ?)'
        # b) Ejecutare la consulta
        pwd = generate_password_hash(pwd)
        res = accion(sql, (usr, pwd))
        # c) Verificar el resultado
        if res==0:
            flash('ERROR: No se pudieron guardar los datos')
        else:
            flash('INFO: Los datos fueron grabados satisfactoriamente')
    return render_template('grabar.html')

@web.route('/enviar/', methods=['GET','POST'])
def prueba():
    res = [[1,'esta es una prueba 1',''],
           [2,'esta es una prueba 2',''],
           [3,'esta es una prueba 3','']]
    return render_template('prueba.html',datos=res)
    
if __name__=='__main__':
    web.run(debug=True)