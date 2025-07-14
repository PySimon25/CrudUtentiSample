from dataclasses import dataclass
from datetime import date

# Questo DTO viene utilizzato solo per restituire dati del prestito
@dataclass
class PrestitoDettaglio:
    id_prestito: int
    data_prestito: date
    data_restituzione_prevista: date
    data_restituzione_effettiva: date | None
    nome_utente: str
    cognome_utente: str
    titolo: str
    autore: str
    isbn: str
    nome_biblioteca: str
    nome_bibliotecario: str
    cognome_bibliotecario: str
