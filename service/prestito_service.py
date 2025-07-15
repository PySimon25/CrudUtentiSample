from repository import PrestitoDAOInterface
from dto import Prestito
from datetime import date

class PrestitoService():

    def __init__(self, prestito_dao: PrestitoDAOInterface) -> None:
        self._dao = prestito_dao

    def registra_prestito(self, id_utente: int, id_libro: int, id_biblioteca: int, id_bibliotecario: int, data_prevista: date) -> int:
        p = Prestito()
        p.utente.id_utente = id_utente
        p.libro.id_libro = id_libro
        p.biblioteca.id_biblioteca = id_biblioteca
        p.bibliotecario.id_bibliotecario = id_bibliotecario
        p.data_prestito = date.today()
        p.data_restituzione_prevista = data_prevista
        return self._dao.assegna_prestito(p)

    def recupera_prestito(self, id: int) -> Prestito | None:
        return self._dao.get_by_id(id)

    def recupera_prestiti_utente(self, id_utente: int) -> list['Prestito']:
        return self._dao.get_by_id_utente(id_utente)