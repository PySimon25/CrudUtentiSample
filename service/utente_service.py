from repository import UtenteDAOInterface
from domain import UtenteBusiness
from dto import Utente
from exceptions import EmailGiaRegistrataError

class UtenteService():

    def __init__(self, utente_dao: UtenteDAOInterface) -> None:
        self._dao = utente_dao

    def recupera_tutti(self) -> list[Utente]:
        return self._dao.get_all()

    def recupera_utente(self, id: int) -> Utente | None:
        return self._dao.get_by_id(id)
    
    def registra_utente(self, nome: str, cognome: str, email: str, telefono: str) -> int:
        dto = Utente()
        ub = UtenteBusiness(dto)

        # Valida i dati
        ub.nome = nome
        ub.cognome = cognome
        ub.email = email
        ub.telefono = telefono

        # Controllo per email già registrata sul database
        if self._dao.find_by_email(email) is not None:
            raise EmailGiaRegistrataError(email)        

        return self._dao.create(ub.to_dto())

    def rimuovi_utente(self, id: int) -> bool:
        return self._dao.delete(id)
    
    def cerca_email(self, email: str) -> Utente | None:
        return self._dao.find_by_email(email)
