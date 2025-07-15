from dataclasses import dataclass

# Transfer Object (DTO) per Categoria
@dataclass
class Categoria:
    id_categoria: int | None = None
    nome_categoria: str | None = None
