from flask import Flask,render_template,request,redirect,url_for,flash
from pymysql import *

app = Flask(__name__)

#Coneccion Mysql
conexion = connect(
    host = 'localhost',
    user = 'admin', 
    password = 'admin', 
    database = 'contact_flask',
    charset = 'utf8mb4',
    cursorclass = cursors.DictCursor)

#Configuraciones
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    sql = 'SELECT * FROM contacts '
    cursor = conexion.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html',contacts = data)

@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        try:
            with  conexion.cursor() as cursor:
                sql = 'INSERT INTO contacts(fullname,phone,email)VALUES(%s,%s,%s)'
                cursor.execute(sql,(fullname,phone,email))
                conexion.commit()
                flash('Contacto Registrado con Exito')
                cursor.close()
        finally:
            cursor.close()        

        return redirect(url_for('index'))

@app.route('/edit/<string:id>')
def edit_contact(id):
    cursor = conexion.cursor() 
    sql = 'SELECT * FROM contacts WHERE id = %s '
    cursor.execute(sql,(id))
    data = cursor.fetchall()
    print(data[0])
    return render_template('update.html',contact = data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = conexion.cursor()
        sql = 'UPDATE contacts SET fullname = %s,phone = %s,email = %s WHERE id = %s'
        cursor.execute(sql,(fullname,phone,email,id))
        conexion.commit()
        flash('Contacto Actualizado con Exito')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = conexion.cursor() 
    sql = 'DELETE FROM contacts WHERE id = {0}'.format(id)
    cursor.execute(sql)
    conexion.commit()
    flash('Contacto Eliminado con Exito')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=3000,debug=True)