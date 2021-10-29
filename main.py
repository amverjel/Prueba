from os import error
from sqlite3.dbapi2 import connect
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask import g
from forms import Formulario_Login
from flask import session
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from utils import isUsernameValid, isEmailValid, isPasswordValid
import yagmail as yagmail
import os
from db import get_db, close_db
from database import sql_select_productos, sql_insert_productos

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template("Inicio.html")

# Usuario requerido:
# Es como si se estuviese llamando directamente a la función interna
def login_required(view):
    @functools.wraps( view ) # toma una función utilizada en un decorador y añadir la funcionalidad de copiar el nombre de la función.
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'Administrativo' ) )
        return view( **kwargs )
    return wrapped_view



@app.route('/Registro_Administrativo', methods=['GET', 'POST'])
def Registro_Administrativo():
    try:
        if request.method == 'POST':
            db = get_db()
            nombre = request.form['Nombre']
            apellido = request.form['Apellido']
            documento = request.form['Documento']   
            email = request.form['Email']
            usuario = request.form['Nombre_de_usuario']
            confirmar_usu = request.form['Nombre_de_usuario1']
            contraseña = request.form['Contraseña']
            confirmar_con = request.form['Contraseña1']
            user = db.execute('SELECT * FROM administrador WHERE nombre_usuario = ? or email = ?  ', (usuario,email) ).fetchone()

            error = None
            if usuario==confirmar_usu and contraseña==confirmar_con:

                if not isUsernameValid(usuario):
                    error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                    flash(error)
                if not isEmailValid(email):
                    error = 'Correo invalido'
                    flash(error)
                if not isPasswordValid(contraseña):
                    error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
                    flash(error)

            else:
                error = 'Usuario o contraseña no coinciden'

            if user is not None:
                error='Nombre de usuario o email ya existen'
                flash(error)
    
            if error is not None:
                return render_template("Registro_Administrativo.html")
            else:
                print("hola")
                # Modificar la siguiente linea con tu informacion personal
                #pehernaldo2@gmail.com  Hernaldo12345678*
                password_cifrado = generate_password_hash(contraseña)
                db.execute('INSERT INTO administrador (nombre, apellido, documento, email, nombre_usuario, password) VALUES (?,?,?,?,?,?)',(nombre, apellido, documento, email, usuario, password_cifrado))
                db.commit()
                yag = yagmail.SMTP('aeropuertoelalcaravan@gmail.com', 'aeropuerto123') 
                yag.send(to=email, subject='Activa tu cuenta',
                    contents='Bienvenido, usa este link para activar tu cuenta')
                flash('Revisa tu correo para activar tu cuenta.') 
                return redirect( ( 'Administrativo' ) )
        
        else:

            return render_template("Registro_Administrativo.html")
    except:

        return render_template("Registro_Administrativo.html")

@app.route('/Inicio-Administrativo', methods=['GET', 'POST'])
@login_required
def Inicio_Administrativo():
    return render_template("Inicio-Administrativo.html")

@app.route('/Crear_piloto', methods=['GET', 'POST'])
@login_required
def Crear_piloto():
    try:
        if request.method == 'POST':  
            db = get_db()     
            nombre = request.form['nombre']
            apellidos=request.form['apellidos']
            cedula = request.form['cedula']
            correo=request.form['correo']
            codigopiloto=request.form['codpiloto']
            db.execute('INSERT INTO pilotos (nombre,apellido,cedula,correo,codigopiloto) VALUES (?,?,?,?,?)',(nombre,apellidos,cedula,correo,codigopiloto))
            db.commit()   
            flash('Piloto creado con éxito')
            return redirect(url_for("Crear_piloto"))                
        else:
            return render_template("Crear_piloto.html")
    except:
        return render_template("Crear_piloto.html")

@app.route('/Editar', methods=['GET', 'POST'])
@login_required
def Editar():
    try:
        if request.method == 'POST':  
            db = get_db()     
            nombre = request.form['nombre']
            apellidos=request.form['apellidos']
            cedula = request.form['cedula']
            correo=request.form['correo']
            codigopiloto=request.form['codpiloto']
            db.execute('UPDATE pilotos SET nombre = ?,apellido = ?,cedula = ?,correo = ?,codigopiloto = ? WHERE  codigopiloto = ?',(nombre,apellidos,cedula,correo,codigopiloto,codigopiloto))
            db.commit()   
            flash('Piloto Editado con éxito')
            return redirect(url_for("Editar"))                
        else:
            return render_template("Editar.html")
    except:
        return render_template("Editar.html")

@app.route('/Eliminar', methods=['GET', 'POST'])
@login_required
def Eliminar():
    try:
        if request.method == 'POST':  
            db = get_db()     
            codigopiloto=request.form['codpiloto']
            print(codigopiloto)
            db.execute('DELETE FROM pilotos WHERE codigopiloto = ?',(codigopiloto,))
            db.commit()   
            print('DELETE FROM pilotos WHERE codigopiloto = ?',(codigopiloto))
            flash('Piloto Eliminado con éxito')
            return redirect(url_for("Eliminar"))                
        else:
            return render_template("Eliminar.html")
    except:
        return render_template("Eliminar.html")

@app.route('/UsuariosAdministrador', methods=['GET', 'POST'])
@login_required
def UsuariosAdministrador():
        sql="SELECT  nombre,edad,sexo FROM usuarios"
        usuarios=sql_select_productos(sql)
        return render_template("UsuariosAdministrador.html",usuarios=usuarios)

@app.route('/Vuelosm', methods=['GET', 'POST'])
@login_required
def Vuelosm():
        sql="SELECT *FROM vuelos"
        vuelos=sql_select_productos(sql)
        return render_template("Vuelosm.html",vuelos=vuelos)

@app.route('/Administrativo',methods=['GET', 'POST'])
def Administrativo():
    try:
        if request.method == 'POST':  
            db = get_db()     
            username = request.form['username']
            password=request.form['password']
            error=None
            user = db.execute('SELECT * FROM administrador WHERE nombre_usuario = ? ', (username,) ).fetchone()
            if user is None:
                error = "Usuario no existe."
                flash(error) 
                return render_template("Administrativo.html")
            else:      
                password_correcto = check_password_hash(user[6],password)  
                if not password_correcto:
                    error='Usuario y/o contraseña no son correctos.'
                    flash(error)     
                    return render_template("Administrativo.html")
                else:
                    session.clear()
                    session['nombre_usuario'] = user[5]
                    return redirect(url_for('Inicio_Administrativo') )                  
        else:
            return render_template("Administrativo.html")
    except:
        return render_template("Administrativo.html")

@app.route('/Gestion_Comentarios', methods=['GET', 'POST'])
@login_required
def Gestión_Comentarios():
        sql="SELECT idComentario, nombre, apellido,FKIdVuelo, calificacion,correo,comentario FROM comentarios"
        comentarios=sql_select_productos(sql)
        print(comentarios)
        return render_template("Gestion_Comentarios.html",comentarios=comentarios)

@app.route('/Crear_Vuelo', methods=['GET', 'POST'])
@login_required
def Crear_Vuelo():
    try:
        if request.method == 'POST':  
            db = get_db()     
            cod_vuelo = request.form['ciudad_origen']
            ciu_origen=request.form['ciudad_origen']
            ciu_destino = request.form['ciudad_destino']
            hora_salida=request.form['hora_salida']
            hora_llegada=request.form['hora_llegada']
            avion=request.form['avion']
            capacidad=request.form['capacidad']
            estado_vuelo=request.form['estado_vuelo']
            db.execute('INSERT INTO vuelos (codigoVuelo, origen, destino, horaSalida,horaLlegada,avion,capacidad,FKestadoVuelo) VALUES (?,?,?,?,?,?,?,?)',(cod_vuelo, ciu_origen, ciu_destino, hora_salida,hora_llegada,avion,capacidad,estado_vuelo))
            db.commit()   
            flash('Vuelo creado con éxito')
            return redirect(url_for("Crear_Vuelo"))                
        else:
            return render_template("Crear_Vuelo.html")
    except:
        return render_template("Crear_Vuelo.html")

@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():
    return render_template("Dashboard.html")

@app.route('/Buscar-vuelos', methods=['GET', 'POST'])
def Buscar_vuelos():
    return render_template("Buscar-vuelos.html")

@app.route('/contactenos', methods=['GET', 'POST'])
def contactenos():
    return render_template("contactenos.html")

@app.route('/about-us', methods=['GET', 'POST'])
def about_us():
    return render_template("about-us.html")

@app.route('/2Eliminar-vuelo', methods=['GET', 'POST'])
def Eliminar_vuelo():
    return render_template("2Eliminar-vuelo.html")

@app.route('/Editar-vuelo', methods=['GET', 'POST'])
def Editar_vuelo():
    return render_template("Editar-vuelo.html")

@app.route('/Calificacion', methods=['GET', 'POST'])
def Calificacion():
    try:
        if request.method == 'POST':  
            nombre = request.form['nombre']
            apellido=request.form['apellidos']
            vuelo = request.form['vuelo']
            cod_vuelo="SELECT * FROM vuelos where codigoVuelo='{}'".format(vuelo)
            codigo=sql_select_productos(cod_vuelo)
            calificacion=request.form['calificacion']
            correo=request.form['correo']
            comentario=request.form['comentario']
            datos=("INSERT INTO comentarios (nombre,apellido,FKIdVuelo,calificacion,correo,comentario) VALUES ('{}','{}','{}','{}','{}','{}')".format(nombre, apellido, codigo[0][0], calificacion,correo,comentario)) 
            sql_insert_productos(datos)
            flash('Calificación creada con éxito') 
            return render_template("Calificacion.html")              
        else:
            return render_template("Calificacion.html")
    except:
        return render_template("Calificacion.html")

@app.route('/Registro', methods=['GET', 'POST'])
def Registro():
    return render_template("Registro.html")

@app.route('/Iniciar-sesion', methods=['GET', 'POST'])
def Iniciar_sesion():
    return render_template("Iniciar-sesion.html")

@app.route('/Reservar-vuelo', methods=['GET', 'POST'])
def Reservar_vuelo():
    return render_template("Reservar-vuelo.html")

@app.before_request
def cargar_usuario_registrado():
    id_usuario = session.get('nombre_usuario')

    if id_usuario is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, nombre,apellido,documento,email,nombre_usuario,password FROM administrador where nombre_usuario=?'
            ,
            (id_usuario,)
        ).fetchone()

@app.route('/logout')
def logout():
    session.clear()    
    return redirect( url_for('Administrativo')  )