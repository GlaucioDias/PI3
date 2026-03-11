from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.services.usuario_service import UsuarioService

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = UsuarioService.buscar_usuario_por_email(email)
        
        if usuario and validarSenha(senha, usuario):
            session["logado"] = True
            session["usuario_email"] = email
            flash("Login realizado!")
            return redirect(url_for("main.index"))
        else:
            flash("Usuário ou senha inválidos")

    return render_template("login.html")

def validarSenha(senha, usuario):
    return  check_password_hash(usuario["senha"], senha)

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("Dados do formulário:", request.form)
        nome = request.form.get("nome")
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha")

        if not senha:
            flash("Senha é obrigatória")
            return redirect(url_for("auth.register"))

        senha_hash = generate_password_hash(senha)

        UsuarioService.criar_usuario(nome, email, senha_hash)
        
        try:
            UsuarioService.criar_usuario(nome, email, senha_hash)

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("auth.login"))

        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.register"))

        except Exception:
            flash("Erro interno ao cadastrar usuário", "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html")