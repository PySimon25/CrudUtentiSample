from dataclasses import dataclass, field
from datetime import date
from .biblioteca import Biblioteca
from .bibliotecario import Bibliotecario
from .libro import Libro
from .utente import Utente

# Transfer Object (DTO) per Prestito
@dataclass
class Prestito:
    id_prestito: int | None = None
    biblioteca: Biblioteca = field(default_factory=Biblioteca)
    bibliotecario: Bibliotecario = field(default_factory=Bibliotecario)
    utente: Utente = field(default_factory=Utente)
    libro: Libro = field(default_factory=Libro)
    data_prestito: date = date.today()
    data_restituzione_prevista: date = date.today()
    data_restituzione_effettiva: date | None = None
