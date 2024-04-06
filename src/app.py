from flask import Flask, render_template, request, redirect, url_for, current_app
import os
#se llama el archivo en el que se hizo la conexion a la base de datos
import database as db

#es una variable especial en Python que contiene la ruta del archivo actual
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

#Esta línea de código está creando una instancia de la aplicación Flask y configurando la carpeta de plantillas (templates) de la aplicación.
app = Flask(__name__, template_folder = template_dir)


@app.route('/') #Este es el que permite configurar la de ruta en Flask 
# Esta función se ejecutará cuando un usuario acceda a la ruta especificada
def home():  # se crea la funcion que 
    current_app.logger.info("home") # solo son comentarios para que se vea desde la terminal 
    # yo los use para ver en que parte del codigo se detiene la aplicacion
    return render_template('index.html') # Flask toma el nombre de la plantilla como argumento y devuelve el contenido HTML generado por esa plantilla

@app.route('/cuenta')
def cuenta():
    return render_template('cuenta.html')

@app.route('/movimiento')
def movimiento():
    return render_template('movimiento.html')

app.route('/lista_usuarios')
def  listaUsuarios():
    return render_template('listaUsuario.html')
   # hasta aca se repite todo lo anterior  

#crear usuario  
@app.route('/usuario', methods=['POST'])#Este es el que permite configurar la de ruta que el usuario vera cuando 
#llegue a esta ruta el methods permite realizar el envio de los datos 
def agregarUsuario():
    current_app.logger.info("---usuario----") #solo comentarios
    nombre = request.form['nombre'] 
    '''se guarda en una variable lo que agregue el usuario ingrese en el input que pertenece a este 
    se utiliza en Flask para acceder a los datos enviados desde un formulario HTML utilizando el método POST.'''
    current_app.logger.info(nombre)
    identificacion = request.form['identificacion']
    clave = request.form['clave']
    
    if nombre and identificacion and clave: # si el usuario ingreso los tres valores 
        current_app.logger.info("-----validacion usuario---------")
        cursor = db.database.cursor() # El cursor en el contexto de bases de datos es un objeto que permite
        #ejecutar consultas SQL y manipular los resultados obtenidos de esas consultas. 
        current_app.logger.info("------conexion base de datos en tabla usuario-------")
        sql = "INSERT INTO usuario (nombre, identificacion, clave) VALUES (%s, %s, %s)" # estas son las consultas
        data_usuario = (nombre, identificacion, clave) # solo en una variable se guardan todos los datos que se ingresaron
        cursor.execute(sql, data_usuario) #se utiliza en Python para ejecutar una consulta SQL en una base de datos. 
        # este caso ejecuta la consulta que se hizo y los valos que el usuario ingreso 
        db.database.commit() 
        # Confirmar la transacción para que los cambios se hagan en la base de datos, con los datos que se van a guardar
        current_app.logger.info("------datos del usuario guardados-------")
    return redirect(url_for('cuenta')) #luego redirecciona a la pantalla cuenta
  

# de aca en adelante es lo mismo pero ya con cuenta y movimientos
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

# de aca en adelante no lo he terminado 

#realizar movimiento
@app.route('/movimiento', methods=['GET', 'POST'])
def realizarMovimiento():
    current_app.logger.info("----movimientos----")
    #cursor = db.database.cursor()
    current_app.logger.info("-----conexion base de datos-----")
   # sql = "SELECT saldo FROM cuenta" 
   # current_app.logger.info(sql)
    #cursor.execute()
    
    monto = request.form["monto"] 
    tipo_movimiento =  request.form['tipo_movimiento']
        
    if tipo_movimiento == "consignacion":
        saldo += monto
        current_app.logger.info("nuevo saldo " + saldo)
            
    elif tipo_movimiento == "transaccion":
        if saldo > monto:
            saldo -= monto
            current_app.logger.info("nuevo saldo" + saldo)
        else:
            cursor = db.database.cursor()       
            update_sql = "UPDATE cuenta SET saldo = %s"   
            cursor.execute(update_sql, (saldo))
            db.database.commit()
            cursor.close()
    
    current_app.logger.info("saldo guardado")
        
    return redirect(url_for('movimiento'))
    
    '''
    monto = request.form ["monto"]
    if tipo_cuenta == "consignacion":
       saldo = saldo + monto
       current_app.logger.info(saldo)
       cursor.execute(saldo)
       db.database.commit()
       
    if tipo_cuenta == "transaccion":
        saldo = saldo - monto
        current_app.logger.info(saldo)
        cursor.execute(saldo)
    
    cursor.execute("UPDATE cuenta SET saldo = ? WHERE tipo_cuenta = ?", (saldo, tipo_cuenta))    
    return redirect(url_for('movimiento')) 
  
 
@app.route('/tablaUsuarios', methods=['GET'])
def obtenerUsuarios():
    cursor = db.database.cursor()
    current_app.logger.info("-----se hizo la conexion a la base de datos")
    consulta = "SELECT u.identificacion, u.nombre, c.tipo_cuenta, c.saldo FROM usuario u INNER JOIN cuenta c ON u.identificacion = c.usuario_id"
    cursor.execute(consulta)
    list = cursor.fetchall
    current_app.logger.info("---Se obtuvieron los datos correctamente------")
    insertObject = []
    columnNames = [column [0] for column in cursor.description]
    for recorre in list:
        insertObject.append(dict(zip(columnNames, recorre)))
    return render_template('listaUsuarios.html', cuenta_usuario = list)
    '''

if __name__ == '__main__':
    app.run(debug=True, port=3000)