from app.database import get_db_connection


class EventoRepository:

    @staticmethod
    def listar_eventos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eventos")
        eventos = cursor.fetchall()
        conn.close()
        return eventos


    @staticmethod
    def buscar_evento(evento_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eventos WHERE id = %s", (evento_id,))
        evento = cursor.fetchone()
        conn.close()
        return evento
    
    @staticmethod
    def criar_evento(evento_data: dict):
        """
        evento_data: dict com titulo, descricao, cidade_id, data, horario, endereco, imagem, usuario_id
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                INSERT INTO eventos 
                (titulo, descricao, cidade_id, data, horario, endereco, imagem, usuario_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                evento_data.get("titulo"),
                evento_data.get("descricao"),
                evento_data.get("cidade_id"),
                evento_data.get("data"),
                evento_data.get("horario"),
                evento_data.get("endereco"),
                evento_data.get("imagem"),
                evento_data.get("usuario_id")
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao criar evento: {e}")
            return False