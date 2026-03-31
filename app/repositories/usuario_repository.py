
from app.database import get_db_connection

class UsuarioRepository:

    @staticmethod
    def buscar_usuario_por_email(email):
        if email is None:
            return None
        email = email.strip().lower()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    @staticmethod
    def criar_usuario(nome, email, senha_hash, tipo='usuario'):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, senha_hash, tipo))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False
    @staticmethod
    def listar_usuarios():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, tipo, created_at FROM usuarios ORDER BY created_at DESC")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    
    @staticmethod
    def atualizar_tipo_usuario(usuario_id, tipo):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "UPDATE usuarios SET tipo = %s WHERE id = %s"
            cursor.execute(sql, (tipo, usuario_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao atualizar tipo de usuário: {e}")
            return False