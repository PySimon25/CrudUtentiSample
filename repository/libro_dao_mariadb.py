import mariadb
from dto import Biblioteca, Categoria, Genere, Libro
from repository import LibroDAOInterface

class LibroDAOMariaDB(LibroDAOInterface):

    def __init__(self, pool: mariadb.ConnectionPool) -> None:
        self.pool = pool

    def create(self, libro: Libro) -> int:
        """Implementa l'operazione CREATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execite(
                    """INSERT INTO Libri (id_biblioteca, titolo, autore, anno_pubblicazione, isbn, id_categoria, id_genere)
                    VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (libro.biblioteca.id_biblioteca, libro.titolo, libro.autore, libro.anno_pubblicazione, libro.isbn, libro.categoria.id_categoria, libro.genere.id_genere)
                )
                conn.commit()
                newid = cursor.lastrowid
                if newid is None:
                    raise RuntimeError("L'inserimento non ha restituito un ID.")
                return newid
        finally:
            conn.close()

    def get_by_id(self, id_libro: int) -> Libro | None:
        """Implementa l'operazione READ per ID"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT li.id_libro, li.titolo, 
                               li.autore, li.anno_pubblicazione, li.isbn, ca.id_categoria, ca.nome_categoria, ge.id_genere, ge.nome_genere,
                               bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo
                               FROM Libri li
                               JOIN Biblioteche bb on bb.id_biblioteca = li.id_biblioteca
                               JOIN Categorie ca on ca.id_categoria = li.id_categoria
                               JOIN Generi ge on ge.id_genere = li.id_genere
                               WHERE li.id_libro = ?""", (id_libro,))
                row = cursor.fetchone()
                return self._row_to_libro(row)
        finally:
            conn.close()
    
    def get_all(self) -> list[Libro]:
        """Implementa l'operazione READ per Libri"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT li.id_libro, li.titolo, 
                               li.autore, li.anno_pubblicazione, li.isbn, ca.id_categoria, ca.nome_categoria, ge.id_genere, ge.nome_genere,
                               bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo
                               FROM Libri li
                               JOIN Biblioteche bb on bb.id_biblioteca = li.id_biblioteca
                               JOIN Categorie ca on ca.id_categoria = li.id_categoria
                               JOIN Generi ge on ge.id_genere = li.id_genere
                               ORDER BY li.titolo""")
                rows = cursor.fetchall()
                return [self._row_to_libro(row) for row in rows]
        finally:
            conn.close()
    
    def update(self, libro: Libro) -> bool:
        """Implementa l'operazione UPDATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE Libri SET id_biblioteca = ?, titolo = ?, autore = ?, anno_pubblicazione = ?, isbn = ?, id_categoria = ?, id_genere = ? WHERE id_libro = ?""",
                    (libro.biblioteca.id_biblioteca, libro.titolo, libro.autore, libro.anno_pubblicazione, libro.isbn, libro.categoria.id_categoria, libro.genere.id_genere, libro.id_libro)
                )
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()
    
    def delete(self, id_libro: int) -> bool:
        """Implementa l'operazione DELETE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM LIbri WHERE id_libro = ?", (id_libro,))
                conn.commit()
                rowcount = cursor.rowcount
                return rowcount > 0
        finally:
            conn.close()

    def _row_to_libro(self, row: dict) -> Libro:
        # Biblioteca alla quale è assegnato il Libro
        libro_biblioteca = Biblioteca(
            id_biblioteca = row['id_biblioteca'],
            nome_biblioteca = row['nome_biblioteca'],
            citta = row['citta'],
            indirizzo = row['indirizzo']
        )

        # Categoria del Libro
        categoria = Categoria(
            id_categoria = row['id_categoria'],
            nome_categoria = row['nome_categoria']
        )

        # Genere del Libro
        genere = Genere(
            id_genere = row['id_genere'],
            nome_genere = row['nome_genere']
        )

        # Libro
        return Libro(
            id_libro = row['id_libro'],
            biblioteca = libro_biblioteca,
            titolo = row['titolo'],
            autore = row['autore'],
            anno_pubblicazione = row['anno_pubblicazione'],
            isbn = row['isbn'],
            genere = genere,
            categoria = categoria
        )