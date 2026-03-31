from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.usuario_service import UsuarioService
from app.utils.auth import admin_required

admin = Blueprint("admin", __name__)

@admin.route("/painel_admin")
@admin_required
def painel_admin():
    usuarios = UsuarioService.listar_usuarios()
    return render_template("painel_admin.html", usuarios=usuarios)

@admin.route("/alterar_tipo/<int:usuario_id>", methods=["POST"])
@admin_required
def alterar_tipo(usuario_id):
    novo_tipo = request.form.get("tipo")
    if novo_tipo not in ["usuario", "admin"]:
        flash("Tipo inválido", "error")
        return redirect(url_for("admin.painel_admin"))

    sucesso = UsuarioService.atualizar_tipo_usuario(usuario_id, novo_tipo)
    if sucesso:
        flash("Tipo de usuário atualizado com sucesso!")
    else:
        flash("Erro ao atualizar tipo de usuário", "error")

    return redirect(url_for("admin.painel_admin"))