import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Conexión a la base de datos
def crear_conexion():
    conn = sqlite3.connect('reservas.db')
    return conn

#Tabla propiedades
def crear_tablas():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        correo TEXT NO
                        T NULL,
                        propiedad_id INTEGER NOT NULL,
                        fecha TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    
def crear_tablas():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        correo TEXT NOT NULL UNIQUE,
                        contraseña TEXT NOT NULL)''')
    conn.commit()
    conn.close()
# Ruta
@app.route('/')
def index():
    crear_tablas()
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM propiedades')
    propiedades = cursor.fetchall()
    conn.close()
    return render_template('index.html', propiedades=propiedades)

# Ruta para procesar reservas
@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    fecha = request.form['fecha']
    propiedad_id = request.form.get('propiedad_id') # Aquí debes pasar el ID de la propiedad seleccionada
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reservas (nombre, correo, propiedad_id, fecha) VALUES (?, ?, ?, ?)',
                   (nombre, correo, propiedad_id, fecha))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        hashed_password = generate_password_hash(contraseña, method='sha256')
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)', (nombre, correo, hashed_password))
        conn.commit()
        conn.close()
        flash('Usuario registrado con éxito')
        return redirect(url_for('login'))
    return render_template('registrar.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        conn = crear_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario and check_password_hash(usuario[3], contraseña):
            session['user_id'] = usuario[0]
            flash('Inicio de sesión exitoso')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
