from repository import UtenteDAOInterface
from dto import Utente

class UtenteService():

    def __init__(self, utente_dao: UtenteDAOInterface) -> None:
        self._dao = utente_dao

    def recupera_tutti(self) -> list[Utente]:
        return self._dao.get_all()

    def recupera_utente(self, id: int) -> Utente | None:
        return self._dao.get_by_id(id)
    
    def rimuovi_utente(self, id: int) -> bool:
        return self._dao.delete(id)
    
    def cerca_email(self, email: str) -> Utente | None:
        return self._dao.find_by_email(email)
