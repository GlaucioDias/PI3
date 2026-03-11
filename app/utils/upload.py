import uuid
import os
from flask import current_app


def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


def salvar_imagem(file):

    extensao = file.filename.rsplit(".", 1)[1].lower()

    nome_unico = f"{uuid.uuid4().hex}.{extensao}"

    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_unico)

    file.save(caminho)

    return nome_unico