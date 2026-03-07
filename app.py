import os
import uuid
import pymysql
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session

# =============================
# INICIALIZAÇÃO DO FLASK
# =============================
app = Flask(__name__)
app.secret_key = "chave-secreta"

# =============================
# CONFIGURAÇÕES
# =============================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================
# CONEXÃO COM BANCO DE DADOS
# =============================
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="pi3",
        cursorclass=pymysql.cursors.DictCursor
    )

# =============================
# LISTA DE EVENTOS (SIMULAÇÃO)
# =============================
# DEFINIR A LISTA ANTES DE QUALQUER ROTA QUE A USE
eventos = [
    {
        "id": 1,
        "titulo": "Exemplo de Evento",
        "cidade": "São Paulo",
        "data": "2026-03-20",
        "horario": "19:00",
        "descricao": "Descrição do evento exemplo",
        "endereco": "Av. Paulista, 1000",
        "imagem": None,
        "imagem_url": None
    }
]

# =============================
# FUNÇÃO AUXILIAR
# =============================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# =============================
# ROTAS
# =============================

@app.route("/")
def index():
    cidade = request.args.get("cidade", "")
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")

    eventos_filtrados = []

    for ev in eventos:
        if cidade and cidade.lower() not in ev["cidade"].lower():
            continue
        if data_inicio and ev["data"] < data_inicio:
            continue
        if data_fim and ev["data"] > data_fim:
            continue
        eventos_filtrados.append(ev)

    eventos_carrossel = eventos_filtrados[:5]

    return render_template(
        "index.html",
        eventos=eventos_filtrados,
        eventos_carrossel=eventos_carrossel,
        cidade=cidade,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Aqui você deve verificar no banco de dados
        session["logado"] = True
        session["usuario_nome"] = email
        session["usuario_email"] = email

        flash("Login realizado com sucesso!")
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta")
    return redirect(url_for("index"))

@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Aqui você deve salvar no banco de dados
        session["logado"] = True
        session["usuario_nome"] = nome
        session["usuario_email"] = email

        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("criar_eventos"))

    return render_template("register.html")

@app.route("/evento/<int:evento_id>")
def evento(evento_id):
    evento = next((e for e in eventos if e["id"] == evento_id), None)

    if not evento:
        flash("Evento não encontrado")
        return redirect(url_for("index"))

    return render_template("evento.html", evento=evento)

@app.route("/criareventos", methods=["GET", "POST"])
def criar_eventos():
    # Verificar se usuário está logado
    if not session.get("logado"):
        flash("Faça login para criar eventos")
        return redirect(url_for("login"))
    
    # Buscar cidades do banco de dados
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM cidades ORDER BY nome")
        cidades = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Erro ao buscar cidades: {e}")
        cidades = [{"nome": "São Paulo"}, {"nome": "Rio de Janeiro"}, {"nome": "Belo Horizonte"}]

    if request.method == "POST":
        titulo = request.form.get("titulo")
        cidade = request.form.get("cidade")
        data = request.form.get("data")
        horario = request.form.get("horario")
        descricao = request.form.get("descricao")
        endereco = request.form.get("endereco")
        
        imagem_nome = None

        # Processar upload de imagem
        file = request.files.get("imagem")

        if file and file.filename and allowed_file(file.filename):
            try:
                # Gerar nome único para o arquivo
                extensao = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                
                # Caminho completo para salvar
                caminho_completo = os.path.join(app.config["UPLOAD_FOLDER"], nome_unico)
                
                # Salvar arquivo
                file.save(caminho_completo)
                
                imagem_nome = nome_unico
                
                print(f"Imagem salva: {caminho_completo}")
                
            except Exception as e:
                print(f"Erro ao salvar imagem: {e}")
                flash("Erro ao fazer upload da imagem. O evento foi criado sem imagem.")
                imagem_nome = None

        # Criar novo evento
        novo_evento = {
            "id": len(eventos) + 1,
            "titulo": titulo,
            "cidade": cidade,
            "data": data,
            "horario": horario,
            "descricao": descricao,
            "endereco": endereco,
            "imagem": imagem_nome
        }

        eventos.append(novo_evento)

        flash("Evento criado com sucesso!")
        return redirect(url_for("index"))

    return render_template("criareventos.html", cidades=cidades)

@app.route("/editarevento/<int:evento_id>", methods=["GET", "POST"])
def editar_evento(evento_id):
    # Verificar se usuário está logado
    if not session.get("logado"):
        flash("Faça login para editar eventos")
        return redirect(url_for("login"))
    
    # Buscar o evento
    evento = next((e for e in eventos if e["id"] == evento_id), None)

    if not evento:
        flash("Evento não encontrado")
        return redirect(url_for("gerenciar_eventos"))

    if request.method == "POST":
        evento["titulo"] = request.form.get("titulo")
        evento["cidade"] = request.form.get("cidade")
        evento["data"] = request.form.get("data")
        evento["horario"] = request.form.get("horario")
        evento["descricao"] = request.form.get("descricao")
        evento["endereco"] = request.form.get("endereco")

        # Processar nova imagem se enviada
        file = request.files.get("imagem")
        if file and file.filename and allowed_file(file.filename):
            try:
                # Apagar imagem antiga se existir
                if evento.get("imagem"):
                    caminho_antigo = os.path.join(app.config["UPLOAD_FOLDER"], evento["imagem"])
                    if os.path.exists(caminho_antigo):
                        os.remove(caminho_antigo)
                
                # Salvar nova imagem
                extensao = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                nome_unico = f"{uuid.uuid4().hex}.{extensao}"
                caminho_completo = os.path.join(app.config["UPLOAD_FOLDER"], nome_unico)
                file.save(caminho_completo)
                
                evento["imagem"] = nome_unico
                
            except Exception as e:
                print(f"Erro ao atualizar imagem: {e}")
                flash("Erro ao atualizar imagem")

        flash("Evento atualizado com sucesso!")
        return redirect(url_for("gerenciar_eventos"))

    return render_template("editarevento.html", evento=evento)

@app.route("/gerenciar_eventos")
def gerenciar_eventos():
    # Verificar se usuário está logado
    if not session.get("logado"):
        flash("Faça login para gerenciar eventos")
        return redirect(url_for("login"))
    
    return render_template("gerenciar_eventos.html", eventos=eventos)

@app.route("/excluir_evento/<int:evento_id>")
def excluir_evento(evento_id):
    # Verificar se usuário está logado
    if not session.get("logado"):
        flash("Faça login para excluir eventos")
        return redirect(url_for("login"))
    
    global eventos
    
    # Encontrar o evento para apagar a imagem
    evento = next((e for e in eventos if e["id"] == evento_id), None)
    
    if evento and evento.get("imagem"):
        try:
            # Apagar arquivo de imagem
            caminho_imagem = os.path.join(app.config["UPLOAD_FOLDER"], evento["imagem"])
            if os.path.exists(caminho_imagem):
                os.remove(caminho_imagem)
                print(f"Imagem apagada: {caminho_imagem}")
        except Exception as e:
            print(f"Erro ao apagar imagem: {e}")
    
    # Remover evento da lista
    eventos = [e for e in eventos if e["id"] != evento_id]
    
    flash("Evento excluído com sucesso!")
    return redirect(url_for("gerenciar_eventos"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        print(f"Erro ao servir imagem {filename}: {e}")
        return "Imagem não encontrada", 404

# =============================
# EXECUTAR APLICAÇÃO
# =============================
if __name__ == "__main__":
    app.run(debug=True)