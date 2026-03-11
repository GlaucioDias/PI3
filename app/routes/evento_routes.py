import os
import uuid

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.services.cidade_service import CidadeService
from app.services.evento_service import EventoService
from app.utils.upload import allowed_file

evento = Blueprint("evento", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../static/uploads")

@evento.route("/evento/<int:evento_id>")
def evento_detalhe(evento_id):
    evento = EventoService.buscar_evento(evento_id)
    return render_template("evento.html", evento=evento)

@evento.route("/criareventos", methods=["GET", "POST"])
def criar_eventos():
    if not session.get("logado"):
        flash("Faça login para criar eventos")
        return redirect(url_for("auth.login"))

    cidades = CidadeService.listar_cidades()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        cidade_id = request.form.get("cidade")
        data = request.form.get("data")
        horario = request.form.get("horario")
        descricao = request.form.get("descricao")
        endereco = request.form.get("endereco")
        usuario_id = session.get("usuario_id")  

        imagem_nome = None
        file = request.files.get("imagem")

        if file and file.filename and allowed_file(file.filename):
            try:
                extensao = file.filename.rsplit('.', 1)[1].lower()
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho_completo = os.path.join(UPLOAD_FOLDER, nome_unico)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(caminho_completo)
                imagem_nome = nome_unico
            except Exception as e:
                print(f"Erro ao salvar imagem: {e}")
                flash("Erro ao fazer upload da imagem. O evento será criado sem imagem.")
                imagem_nome = None

        evento_data = {
            "titulo": titulo,
            "descricao": descricao,
            "cidade_id": cidade_id,
            "data": data,
            "horario": horario,
            "endereco": endereco,
            "imagem": imagem_nome,
            "usuario_id": usuario_id
        }

        sucesso = EventoService.criar_evento(evento_data)
        if sucesso:
            flash("Evento criado com sucesso!")
        else:
            flash("Erro ao criar evento!")

        return redirect(url_for("main.index"))

    return render_template("criareventos.html", cidades=cidades)