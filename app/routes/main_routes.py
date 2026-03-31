from flask import Blueprint, render_template, request, session, flash, redirect, url_for, send_from_directory, current_app
from app.services.evento_service import EventoService
from app.services.cidade_service import CidadeService


from app.utils.upload import allowed_file

main = Blueprint("main", __name__)

@main.route("/")
def index():
    eventos = EventoService.listar_eventos()

    cidade = request.args.get("cidade", "")
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")

    eventos_filtrados = []
    for evento in eventos:
       if cidade and evento.get("cidade") and cidade.lower() not in evento["cidade"].lower():
            continue
       if data_inicio and evento["data"] < data_inicio:
            continue
       if data_fim and evento["data"] > data_fim:
            continue
       eventos_filtrados.append(evento)

    eventos_carrossel = eventos_filtrados[:5]

    return render_template(
        "index.html",
        eventos=eventos_filtrados,
        eventos_carrossel=eventos_carrossel,
        cidade=cidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


@main.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")

@main.route("/gerenciar_eventos")
def gerenciar_eventos():
    if not session.get("logado"):
        flash("Faça login para gerenciar eventos")
        return redirect(url_for("auth.login"))
    usuario_id = session.get("usuario_id")
    eventos = EventoService.listar_eventos_por_usuario(usuario_id)
    return render_template("gerenciar_eventos.html", eventos=eventos)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

