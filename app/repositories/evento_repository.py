from app.database import get_db_connection


class EventoRepository:

    @staticmethod
    def listar_eventos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.titulo, e.descricao, e.cidade_id, c.nome AS cidade,
                   DATE(e.data) AS data, e.horario, e.endereco, e.imagem, e.usuario_id
            FROM eventos e
            LEFT JOIN cidades c ON e.cidade_id = c.id
        """)
        eventos = cursor.fetchall()
        conn.close()
        return eventos


    @staticmethod
    def listar_eventos_por_usuario(usuario_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.titulo, e.descricao, e.cidade_id, c.nome AS cidade,
                   DATE(e.data) AS data, e.horario, e.endereco, e.imagem, e.usuario_id
            FROM eventos e
            LEFT JOIN cidades c ON e.cidade_id = c.id
            WHERE e.usuario_id = %s
        """, (usuario_id,))
        eventos = cursor.fetchall()
        conn.close()
        return eventos
    
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
            evento_id = cursor.lastrowid
            conn.close()
            return evento_id
        except Exception as e:
            print(f"Erro ao criar evento: {e}")
            return None

    @staticmethod
    def buscar_evento(evento_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.titulo, e.descricao, e.cidade_id, c.nome AS cidade,
                       DATE(e.data) AS data, e.horario, e.endereco, e.imagem, e.usuario_id
                FROM eventos e
                LEFT JOIN cidades c ON e.cidade_id = c.id
                WHERE e.id = %s
            """, (evento_id,))
            evento = cursor.fetchone()
            conn.close()
            return evento
        except Exception as e:
            print(f"Erro ao buscar evento: {e}")
            return None

    @staticmethod
    def atualizar_evento(evento_id, evento_data: dict):
        """
        evento_data: dict com titulo, descricao, cidade_id, data, horario, endereco, imagem
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                UPDATE eventos 
                SET titulo=%s, descricao=%s, cidade_id=%s, data=%s, horario=%s, endereco=%s, imagem=%s
                WHERE id=%s
            """
            cursor.execute(sql, (
                evento_data.get("titulo"),
                evento_data.get("descricao"),
                evento_data.get("cidade_id"),
                evento_data.get("data"),
                evento_data.get("horario"),
                evento_data.get("endereco"),
                evento_data.get("imagem"),
                evento_id
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao atualizar evento: {e}")
            return False

    @staticmethod
    def excluir_evento(evento_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM eventos WHERE id = %s"
            cursor.execute(sql, (evento_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao excluir evento: {e}")
            return False