from dataclasses import dataclass
from datetime import date

# Transfer Object (DTO) per Prestito
@dataclass
class Prestito:
    id_prestito: int | None = None
    id_biblioteca: int = 0
    id_bibliotecario: int = 0
    id_utente: int = 0
    id_libro: int = 0
    data_prestito: date = date.today()
    data_restituzione_prevista: date = date.today()
    data_restituzione_effettiva: date | None = None
