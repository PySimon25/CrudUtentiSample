from dataclasses import dataclass, field
from .biblioteca import Biblioteca

# Transfer Object (DTO) per Bibliotecario
@dataclass
class Bibliotecario:
    id_bibliotecario: int | None = None
    biblioteca: Biblioteca = field(default_factory=Biblioteca)
    nome: str | None = None
    cognome: str | None = None
    email: str | None = None
