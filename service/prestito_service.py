from repository import PrestitoDAOInterface
from dto import Prestito, PrestitoDettaglio
from datetime import date

class PrestitoService():

    def __init__(self, prestito_dao: PrestitoDAOInterface) -> None:
        self._dao = prestito_dao

    def registra_prestito(self, id_utente: int, id_libro: int, id_biblioteca: int, id_bibliotecario: int, data_prevista: date) -> int:
        return self._dao.assegna_prestito(id_utente, id_libro, id_biblioteca, id_bibliotecario, data_prevista)

    def recupera_prestito(self, id: int) -> Prestito | None:
        return self._dao.get_by_id(id)
    
    def recupera_dettaglio_prestito(self, id: int) -> PrestitoDettaglio | None:
        return self._dao.get_dettaglio_by_id(id)

    def recupera_prestiti_utente(self, id_utente: int) -> list['Prestito']:
        return self._dao.get_by_id_utente(id_utente)

    def recupera_dettaglio_prestiti_utente(self, id_utente: int) -> list['PrestitoDettaglio']:
        return self._dao.get_dettagli_by_id_utente(id_utente)