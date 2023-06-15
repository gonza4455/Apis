from  flask import Flask,jsonify, request
import pymssql
app = Flask(__name__)
conn    = pymssql.connect(
                'jvpdatos.database.windows.net',
                'jcverni@jvpsa.onmicrosoft.com@jvpdatos',
                'JVP4455jvp',
                'Laboratorio'
            )
cursor = conn.cursor()
@app.route("/")
def Chequeo():
    return "Funciona Bien"
@app.route("/Conecto")
def listar_usuarios():
    try:
        cursor.execute("SELECT Nombre, Apellido, Organizacion, Password, Mail FROM Usuarios_Generales")
        regUsuarios = cursor.fetchall()
        Usuarios=[]
        for fila in regUsuarios:
            Usuario = {'Nombre': fila[0],'Apellido':fila[1],'Organizacion':fila[2],'Password':fila[3],'Mail':fila[4]}
            Usuarios.append(Usuario)
        return jsonify({'Data':Usuarios,'Mensaje':'Usuarios Listados'})
    except Exception as ex:
        return jsonify({'Mensaje':f'Error {ex}'})
@app.route("/Conecto/<mail>/<passw>",methods=['GET'])
def leer_usuario(mail,passw):
    try:
        cursor.execute(f"SELECT Nombre, Apellido, Organizacion, Mail, Password FROM Usuarios_Generales WHERE Mail = '{mail}' AND Password ='{passw}'")
        Datos = cursor.fetchone()
        if(Datos != None):
            Usuario = {'Nombre': Datos[0],'Apellido':Datos[1],'Organizacion':Datos[2], 'Mail': Datos[3], 'Password': Datos[4]}
            return jsonify({'Data':Usuario,'Encontrado':True})
        else:
            return jsonify({'Encontrado':False})
        
    except Exception as ex:
        return jsonify({'Mensaje':f'Error {ex}'})
    
@app.route("/Conecto",methods=['POST'])
def agregar_usuario():
    try:
        cursor.execute(f"""INSERT INTO Usuarios_Generales (Nombre, Apellido, Organizacion, Password, Mail)
        VALUES ('{request.json['Nombre']}', '{request.json['Apellido']}', '{request.json['Organizacion']}', '{request.json['Password']}', '{request.json['Mail']}')
        """)
        conn.commit()
        return jsonify({'Mensaje':'Se registro con éxito'})
    except Exception as ex:
        return jsonify({'Mensaje':f'Error{ex}'})
@app.route("/Conecto/<mail>",methods=['DELETE'])
def eliminar_usuario(mail):
    try:
        cursor.execute(f"DELETE Usuarios_Generales WHERE Mail = '{mail}'")
        conn.commit()
        return jsonify({'Mensaje':'Se ha eliminado con éxito'})
    except Exception as ex:
        return jsonify({'Mensaje':f'Error{ex}'})
@app.route("/Conecto/<mail>",methods=['PUT'])
def actualizar_usuario(mail):
    try:
        cursor.execute(f"""UPDATE Usuarios_Generales 
        SET Nombre = '{request.json['Nombre']}', Apellido = '{request.json['Apellido']}', Organizacion = '{request.json['Organizacion']}' 
        WHERE Mail = '{mail}'""")
        conn.commit()
        return jsonify({'Mensaje':'Se actualizó con éxito'})
    except Exception as ex:
        return jsonify({'Mensaje':f'Error{ex}'})

def pagina_no_encontrada(error):
    return '<h1>La Pagina no fue encontrada<h1>'
if __name__ == "__main__":
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True)