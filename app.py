from flask import Flask, redirect, render_template, request, session, url_for
import json
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.secret_key = "holahola123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_USUARIOS = os.path.join(BASE_DIR, "usuarios.json")

@app.route("/")
def raiz():
    return render_template("index.html")


@app.route("/main")
def main():
    if "usuario_conectado" in session:
        return render_template("main.html", nom=session["usuario_conectado"])
    else:
        return render_template("index.html", msg="no has iniciado sesion")

"""
@app.route("/registro")
def pagina_registro():
    return render_template("registro.html")
"""

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]
    try:
        with open(RUTA_USUARIOS,"r",encoding="utf-8") as archivo_usuarios:
            listado = json.load(archivo_usuarios)
    except FileNotFoundError:
        listado = []
    
    for item in listado:
        if item["usuario"] == usuario:
            if check_password_hash(item["contrasena"], contrasena):
                session["usuario_conectado"] = item["nombre"]
                return render_template("main.html", nom=item["nombre"])
            else:
                return render_template("index.html", msg="datos incorrectos")
    
    return render_template("index.html", msg="datos incorrectos")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        usuario = request.form.get("usuario", "").strip()
        nueva_contrasena = request.form.get("contrasena", "")

        if len(nombre) < 3:
            return render_template("registro.html", error="deben ser al menos 3 letras!")
        
        if len(usuario) < 4:
            return render_template("registro.html", error="deben ser al menos 4 caracteres!")
        
        if len(nueva_contrasena) < 6:
            return render_template("registro.html", error="la contraseña debe tener al menos 6 caracteres!")


        try:
            with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
                listado = json.load(archivo)
        except:
            listado = []

        for u in listado:
            if u["usuario"] == usuario:
                return render_template("registro.html", error="el nombre de usuario no esta disponible!")

        contrasena_encrip = generate_password_hash(nueva_contrasena)

        nuevo_usuario = {
            "nombre": nombre,
            "usuario": usuario,
            "contrasena": contrasena_encrip
        }
        listado.append(nuevo_usuario)

        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
            json.dump(listado, archivo, indent=4)
        
        return render_template("index.html", msg="registro exitoso")
    return render_template("registro.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("raiz"))


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)