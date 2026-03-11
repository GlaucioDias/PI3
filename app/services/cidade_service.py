from app.repositories.cidade_repository import CidadeRepository

class CidadeService:

    @staticmethod
    def listar_cidades():
        return CidadeRepository.listar_cidades()