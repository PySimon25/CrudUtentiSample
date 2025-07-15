import mariadb
from dto import Biblioteca, Bibliotecario, Libro, Prestito, Utente
from repository import PrestitoDAOInterface

# Implementazione concreta del DAO
class PrestitoDAOMariaDB(PrestitoDAOInterface):

    def __init__(self, pool: mariadb.ConnectionPool) -> None:
        self.pool = pool

    def assegna_prestito(self, prestito: Prestito) -> int:
        """Implementa l'operazione CREATE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Prestiti (id_utente, id_libro, id_biblioteca, id_bibliotecario, data_prestito, data_restituzione_prevista)
                    VALUES(?, ?, ?, ?, ?, ?)""",
                    (prestito.utente.id_utente, prestito.libro.id_libro, prestito.biblioteca.id_biblioteca, prestito.bibliotecario.id_bibliotecario, 
                     prestito.data_prestito, prestito.data_restituzione_prevista)
                )
                conn.commit()
                newid = cursor.lastrowid
                if newid is None:
                    raise RuntimeError("L'inserimento non ha restituito un ID.")
                return newid
        finally:
            conn.close()  

    def get_by_id(self, id_prestito: int) -> Prestito | None:
        """Implementa l'operazione READ per ID PRESTITO"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT pr.id_prestito, pr.data_prestito, pr.data_restituzione_prevista, pr.data_restituzione_effettiva, 
                               ut.id_utente, ut.nome nome_utente, ut.cognome cognome_utente, ut.email, ut.telefono, li.id_libro, li.titolo, 
                               li.autore, li.anno_pubblicazione, li.isbn, bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo, 
                               bi.id_bibliotecario, bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario, bi.email
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               WHERE id_prestito = ?""", (id_prestito,))
                row = cursor.fetchone()
                return self._row_to_prestito(row)
        finally:
            conn.close()

    def get_by_id_utente(self, id_utente: int) -> list[Prestito]:
        """Implementa l'operazione READ per ID UTENTE"""
        conn = self.pool.get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT pr.id_prestito, pr.data_prestito, pr.data_restituzione_prevista, pr.data_restituzione_effettiva, 
                               ut.id_utente, ut.nome nome_utente, ut.cognome cognome_utente, ut.email, ut.telefono, li.id_libro, li.titolo, 
                               li.autore, li.anno_pubblicazione,  li.isbn, bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo, 
                               bi.id_bibliotecario, bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario, bi.email
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               WHERE pr.id_utente = ?""", (id_utente,))
                rows = cursor.fetchall()
                return [self._row_to_prestito(row) for row in rows]
        finally:
            conn.close()

    def _row_to_prestito(self, row: dict) -> Prestito:
        # Per popolare oggetti complessi non è possibile usare
        # return Prestito(**row) if row else None  /  return [Prestito(**row) for row in rows]
        utente = Utente(
            id_utente = row['id_utente'],
            nome = row['nome_utente'],
            cognome = row['cognome_utente'],
            email = row['email'],
            telefono = row['telefono']
        )

        biblioteca = Biblioteca(
            id_biblioteca = row['id_biblioteca'],
            nome_biblioteca = row['nome_biblioteca'],
            citta = row['citta'],
            indirizzo = row['indirizzo']
        )

        bibliotecario = Bibliotecario(
            id_bibliotecario = row['id_bibliotecario'],
            nome = row['nome_bibliotecario'],
            cognome = row['cognome_bibliotecario']
        )

        libro = Libro(
            id_libro = row['id_libro'],
            titolo = row['titolo'],
            autore = row['autore'],
            anno_pubblicazione = row['anno_pubblicazione'],
            isbn = row['isbn']
        )

        return Prestito(
            id_prestito = row['id_prestito'],
            biblioteca = biblioteca,
            bibliotecario = bibliotecario,
            utente = utente,
            libro = libro,
            data_prestito = row['data_prestito'],
            data_restituzione_prevista = row['data_restituzione_prevista'],
            data_restituzione_effettiva = row['data_restituzione_effettiva']
        )