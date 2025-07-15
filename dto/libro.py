from dataclasses import dataclass, field
from .biblioteca import Biblioteca
from .categoria import Categoria
from .genere import Genere

# Transfer Object (DTO) per Libro
@dataclass
class Libro:
    id_libro: int | None = None
    biblioteca: Biblioteca = field(default_factory=Biblioteca)
    titolo: str | None = None
    autore: str | None = None
    anno_pubblicazione: int | None = None
    isbn: str | None = None
    categoria: Categoria = field(default_factory=Categoria)
    genere: Genere = field(default_factory=Genere)
