import os
from datetime import datetime, date, time
from flask import Flask
from .config import Config


def format_date_time_br(data_value, time_value=None):
    """Formata data/hora no padrão brasileiro com milissegundos."""
    if not data_value:
        return ""

    # trata data como string ou objeto date/datetime
    if isinstance(data_value, str):
        try:
            data_obj = datetime.fromisoformat(data_value)
        except ValueError:
            try:
                data_obj = datetime.strptime(data_value, "%Y-%m-%d")
            except ValueError:
                return data_value
    elif isinstance(data_value, date) and not isinstance(data_value, datetime):
        data_obj = datetime.combine(data_value, time.min)
    elif isinstance(data_value, datetime):
        data_obj = data_value
    else:
        return str(data_value)

    # processa horário se fornecido
    if time_value:
        if isinstance(time_value, str):
            fmt = "%H:%M:%S" if len(time_value.split(':')) == 3 else "%H:%M"
            try:
                time_obj = datetime.strptime(time_value, fmt).time()
            except ValueError:
                try:
                    time_obj = datetime.strptime(time_value, "%H:%M:%S.%f").time()
                except ValueError:
                    time_obj = time.min
        elif isinstance(time_value, time):
            time_obj = time_value
        else:
            time_obj = time.min
        data_obj = datetime.combine(data_obj.date(), time_obj)

        # somente horas e minutos para exibição do usuário
        return data_obj.strftime('%d/%m/%Y %H:%M')

    # se data_obj já tem hora diferente de meia-noite, preserva hora e minuto
    if data_obj.hour != 0 or data_obj.minute != 0 or data_obj.second != 0:
        return data_obj.strftime('%d/%m/%Y %H:%M')

    # sem horário (00:00), apenas data BR
    return data_obj.strftime('%d/%m/%Y')


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Registrar blueprints
    from .routes.main_routes import main
    from .routes.auth_routes import auth
    from .routes.evento_routes import evento
    from .routes.admin_routes import admin

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(evento)
    app.register_blueprint(admin)

    # Filtro global para formatar data/hora BR com milissegundos em templates
    app.add_template_filter(format_date_time_br, 'br_datetime')

    return app