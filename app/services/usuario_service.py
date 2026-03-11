from app.repositories.usuario_repository import UsuarioRepository

class UsuarioService:

    @staticmethod
    def buscar_usuario_por_email(email):
        return UsuarioRepository.buscar_usuario_por_email(email)
    
    # @staticmethod
    # def criar_usuario(nome, email, senha_hash):
    #     if UsuarioRepository.buscar_usuario_por_email(email):
    #         raise ValueError("Email já cadastrado")

    #     return UsuarioRepository.criar_usuario(nome, email, senha_hash)

    @staticmethod
    def criar_usuario(nome, email, senha_hash):
        # usuario_existente = UsuarioRepository.buscar_usuario_por_email(email)

        # if usuario_existente:
        #     raise ValueError("Email já cadastrado")
        if UsuarioRepository.buscar_usuario_por_email(email):
            raise ValueError("Email já cadastrado")
        
        return UsuarioRepository.criar_usuario(nome, email, senha_hash)