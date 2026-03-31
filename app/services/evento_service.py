from app.repositories.evento_repository import EventoRepository


class EventoService:

    @staticmethod
    def listar_eventos():
        return EventoRepository.listar_eventos()


    @staticmethod
    def listar_eventos_por_usuario(usuario_id):
        return EventoRepository.listar_eventos_por_usuario(usuario_id)
    
    @staticmethod
    def criar_evento(evento_data):
        return EventoRepository.criar_evento(evento_data)

    @staticmethod
    def buscar_evento(evento_id):
        return EventoRepository.buscar_evento(evento_id)

    @staticmethod
    def atualizar_evento(evento_id, evento_data):
        return EventoRepository.atualizar_evento(evento_id, evento_data)

    @staticmethod
    def excluir_evento(evento_id):
        return EventoRepository.excluir_evento(evento_id)