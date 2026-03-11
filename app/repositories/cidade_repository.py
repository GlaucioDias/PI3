from app.database import get_db_connection

class CidadeRepository:

    @staticmethod
    def listar_cidades():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM cidades ORDER BY nome")
            resultado = cursor.fetchall()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Erro ao buscar cidades: {e}")
            return []