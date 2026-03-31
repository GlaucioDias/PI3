from app.repositories.usuario_repository import UsuarioRepository

class UsuarioService:

    @staticmethod
    def buscar_usuario_por_email(email):
        return UsuarioRepository.buscar_usuario_por_email(email)

    @staticmethod
    def criar_usuario(nome, email, senha_hash, tipo='usuario'):
        if not nome or not email or not senha_hash:
            raise ValueError("Nome, email e senha são obrigatórios")

        email_normalizado = email.strip().lower()
        usuario_existente = UsuarioRepository.buscar_usuario_por_email(email_normalizado)
        if usuario_existente:
            raise ValueError("Email já cadastrado")

        return UsuarioRepository.criar_usuario(nome.strip(), email_normalizado, senha_hash, tipo)

    @staticmethod
    def listar_usuarios():
        return UsuarioRepository.listar_usuarios()
    
    @staticmethod
    def atualizar_tipo_usuario(usuario_id, tipo):
        return UsuarioRepository.atualizar_tipo_usuario(usuario_id, tipo)