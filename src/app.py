from flask import Flask, render_template, request, redirect, url_for, current_app
import os #proporciona una interfaz para interactuar con el sistema operativo. 
import database as db

# configuracion del directorio de plantillas 
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

@app.route('/movimiento')
def movimiento():
    return render_template('movimiento.html')

app.route('/lista_usuarios')
def  listaUsuarios():
    return render_template('listaUsuario.html')
   

#CREAR USUARIO
@app.route('/usuario', methods=['POST'])
def agregarUsuario():
    current_app.logger.info("---usuario----") 
    nombre = request.form['nombre'] 
    current_app.logger.info(nombre)
    identificacion = request.form['identificacion']
    clave = request.form['clave']
    
    if nombre and identificacion and clave:
        current_app.logger.info("-----validacion usuario---------")
        cursor = db.database.cursor() #Aquí se está creando un cursor para la conexión a la base de datos.
        #El cursor se utiliza para ejecutar consultas SQL y manipular los resultados.
        current_app.logger.info("------conexion base de datos en tabla usuario-------")
        sql = "INSERT INTO usuario (nombre, identificacion, clave) VALUES (%s, %s, %s)" 
        data_usuario = (nombre, identificacion, clave) 
        cursor.execute(sql, data_usuario) 
        db.database.commit() 
        current_app.logger.info("------datos del usuario guardados-------")
    return redirect(url_for('cuenta')) 
  
#CREAR CUENTA
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

#REALIZAR MOVIMIENTO
@app.route('/movimiento', methods=['GET', 'POST'])
def realizarMovimiento():
    saldo = 0

    current_app.logger.info("----movimientos----")
    current_app.logger.info("-----conexion base de datos-----")
    monto = request.form["monto"] 
    tipo_movimiento =  request.form['tipo_movimiento']
        
    if tipo_movimiento == "consignacion":
        saldo += monto
        current_app.logger.info("nuevo saldo " + str(saldo))
            
    elif tipo_movimiento == "transaccion":
        if saldo > monto:
            saldo -= monto
            current_app.logger.info("nuevo saldo" + str(saldo))
       
    cursor = db.database.cursor()       
    update_sql = "UPDATE cuenta SET saldo=%s"   
    cursor.execute(update_sql, (saldo, ))
    db.database.commit()
    cursor.close()
    
    current_app.logger.info("-----saldo guardado correctamente-----")
        
    return redirect(url_for('movimiento'))
      
 #LISTA DE USUARIOS     
@app.route('/listaUsuarios', methods=['GET'])
def obtenerUsuarios():
    cursor = db.database.cursor()
    current_app.logger.info("-----se hizo la conexion a la base de datos")
    consulta = "SELECT identificacion, nombre, clave, tipo_cuenta, saldo FROM usuario u INNER JOIN cuenta c ON c.usuario_id = u.identificacion"
    cursor.execute(consulta)
    myResult= cursor.fetchall()
    current_app.logger.info(myResult)
    current_app.logger.info("---Se obtuvieron los datos correctamente------")
    insertObject = []
    columnNames = [column [0] for column in cursor.description]
    #Se obtienen los nombres de las columnas de los resultados de la consulta. Esto es útil para crear un diccionario 
    # que asocie los nombres de las columnas con los valores de cada fila.
    for recorre in myResult: #Se itera sobre los resultados obtenidos de la consulta.
        insertObject.append(dict(zip(columnNames, recorre)))
        # Para cada fila de resultados, se crea un diccionario que asocia cada nombre de columna con su respectivo valor en esa fila. 
        # Este diccionario se añade a la lista insertObject.
    cursor.close()
    return render_template('listaUsuarios.html', data = insertObject)

if __name__ == '__main__':
    app.run(debug=True, port=3000)