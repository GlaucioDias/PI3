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

        novo_evento_id = EventoService.criar_evento(evento_data)
        if novo_evento_id:
            flash("Evento criado com sucesso!")
            return redirect(url_for("evento.evento_detalhe", evento_id=novo_evento_id))
        else:
            flash("Erro ao criar evento!")
            return redirect(url_for("main.index"))

    return render_template("criareventos.html", cidades=cidades)

@evento.route("/editar_evento/<int:evento_id>", methods=["GET", "POST"])
def editar_evento(evento_id):
    if not session.get("logado"):
        flash("Faça login para editar eventos")
        return redirect(url_for("auth.login"))

    evento = EventoService.buscar_evento(evento_id)
    if not evento or evento["usuario_id"] != session.get("usuario_id"):
        flash("Evento não encontrado ou você não tem permissão para editá-lo")
        return redirect(url_for("main.gerenciar_eventos"))

    cidades = CidadeService.listar_cidades()

    if request.method == "POST":
        titulo = request.form.get("titulo")
        cidade_id = request.form.get("cidade")
        data = request.form.get("data")
        horario = request.form.get("horario")
        descricao = request.form.get("descricao")
        endereco = request.form.get("endereco")

        imagem_nome = evento["imagem"]  # Manter a imagem atual por padrão
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
                flash("Erro ao fazer upload da imagem. A imagem atual será mantida.")

        evento_data = {
            "titulo": titulo,
            "descricao": descricao,
            "cidade_id": cidade_id,
            "data": data,
            "horario": horario,
            "endereco": endereco,
            "imagem": imagem_nome,
            "usuario_id": evento["usuario_id"]
        }

        sucesso = EventoService.atualizar_evento(evento_id, evento_data)
        if sucesso:
            flash("Evento atualizado com sucesso!")
        else:
            flash("Erro ao atualizar evento!")

        return redirect(url_for("main.gerenciar_eventos"))

    return render_template("editarevento.html", evento=evento, cidades=cidades)

@evento.route("/excluir_evento/<int:evento_id>", methods=["POST"])
def excluir_evento(evento_id):
    if not session.get("logado"):
        flash("Faça login para excluir eventos")
        return redirect(url_for("auth.login"))

    evento = EventoService.buscar_evento(evento_id)
    if not evento or evento["usuario_id"] != session.get("usuario_id"):
        flash("Evento não encontrado ou você não tem permissão para excluí-lo")
        return redirect(url_for("main.gerenciar_eventos"))

    sucesso = EventoService.excluir_evento(evento_id)
    if sucesso:
        flash("Evento excluído com sucesso!")
    else:
        flash("Erro ao excluir evento!")

    return redirect(url_for("main.gerenciar_eventos"))