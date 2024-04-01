from flask import Flask, render_template, request, redirect, url_for, current_app
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__, template_folder = template_dir)


@app.route('/')
def home():
    current_app.logger.info("home")
    return render_template('index.html')

@app.route('/cuenta')
def cuenta():
    return render_template('cuenta.html')

@app.route('/movimientos')
def movimiento():
    return render_template('movimiento.html')

#crear usuario  
@app.route('/usuario', methods=['POST'])   
def agregarUsuario():
    current_app.logger.info("---usuario----")
    nombre = request.form['nombre']
    current_app.logger.info(nombre)
    identificacion = request.form['identificacion']
    clave = request.form['clave']
    
    if nombre and identificacion and clave:
        current_app.logger.info("-----validacion usuario---------")
        cursor = db.database.cursor()
        current_app.logger.info("------conexion base de datos en tabla usuario-------")
        sql = "INSERT INTO usuario (nombre, identificacion, clave) VALUES (%s, %s, %s)"
        data_usuario = (nombre, identificacion, clave)
        cursor.execute(sql, data_usuario)
        db.database.commit()
        current_app.logger.info("------datos del usuario guardados-------")
    return redirect(url_for('cuenta'))  
  

    
#crear cuenta  
@app.route('/cuenta', methods=['POST'])
def agregarCuenta():
    current_app.logger.info("----cuenta-----")
    tipoCuenta = request.form['tipo_cuenta']
    current_app.logger.info(tipoCuenta)
    

    if tipoCuenta:
        current_app.logger.info("----validacion cuenta-----")
        cursor = db.database.cursor()
        current_app.logger.info("-----conexion con tabla cuenta-------")
        sql = "INSERT INTO cuenta (tipo_cuenta) VALUES (%s)"
        data_cuenta = (tipoCuenta, )
        cursor.execute(sql,data_cuenta)
        db.database.commit()
        current_app.logger.info("-----datos de cuenta guardados------")
    return redirect(url_for('movimiento'))   

#realizar movimiento
@app.route('/movimiento', methods=['GET, POST'])
def realizarMovimiento():
    current_app.logger.info("----movimientos----")
    monto = request.form['monto']
    current_app.logger.info(monto)
    
    

    

if __name__ == '__main__':
    app.run(debug=True, port=3000)