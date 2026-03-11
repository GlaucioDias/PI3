from app.repositories.evento_repository import EventoRepository


class EventoService:

    @staticmethod
    def listar_eventos():
        return EventoRepository.listar_eventos()


    @staticmethod
    def buscar_evento(evento_id):
        return EventoRepository.buscar_evento(evento_id)
    
    @staticmethod
    def criar_evento(evento_data: dict):
        print("Criando evento com os seguintes dados:", evento_data)  # Log para depuração
        # Aqui você poderia validar campos, checar duplicidade, etc
        return EventoRepository.criar_evento(evento_data)