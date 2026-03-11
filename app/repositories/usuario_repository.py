
from app.database import get_db_connection

class UsuarioRepository:

    @staticmethod
    def buscar_usuario_por_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    @staticmethod
    def criar_usuario(nome, email, senha_hash):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, email, senha_hash))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False