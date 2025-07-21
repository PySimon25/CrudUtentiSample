import mariadb
from dto import Biblioteca, Bibliotecario, Categoria, Genere, Libro, Prestito, Utente
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
                               li.autore, li.anno_pubblicazione, li.isbn, ca.id_categoria, ca.nome_categoria, ge.id_genere, ge.nome_genere,
                               bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo,
                               bbl.id_biblioteca libro_biblioteca_id_biblioteca, bbl.nome_biblioteca libro_biblioteca_nome_biblioteca, 
                               bbl.città libro_biblioteca_citta, bbl.indirizzo libro_biblioteca_indirizzo,
                               bi.id_bibliotecario, bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario, bi.email email_bibliotecario,
                               bbb.id_biblioteca bibliotecario_biblioteca_id_biblioteca, bbb.nome_biblioteca bibliotecario_biblioteca_nome_biblioteca,
                               bbb.città bibliotecario_biblioteca_citta, bbb.indirizzo bibliotecario_biblioteca_indirizzo
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bbl on bbl.id_biblioteca = li.id_biblioteca 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               JOIN Biblioteche bbb on bbb.id_biblioteca = bi.id_biblioteca
                               JOIN Categorie ca on ca.id_categoria = li.id_categoria
                               JOIN Generi ge on ge.id_genere = li.id_genere
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
                               li.autore, li.anno_pubblicazione, li.isbn, ca.id_categoria, ca.nome_categoria, ge.id_genere, ge.nome_genere,
                               bb.id_biblioteca, bb.nome_biblioteca, bb.città citta, bb.indirizzo,
                               bbl.id_biblioteca libro_biblioteca_id_biblioteca, bbl.nome_biblioteca libro_biblioteca_nome_biblioteca, 
                               bbl.città libro_biblioteca_citta, bbl.indirizzo libro_biblioteca_indirizzo,
                               bi.id_bibliotecario, bi.nome nome_bibliotecario, bi.cognome cognome_bibliotecario, bi.email email_bibliotecario,
                               bbb.id_biblioteca bibliotecario_biblioteca_id_biblioteca, bbb.nome_biblioteca bibliotecario_biblioteca_nome_biblioteca,
                               bbb.città bibliotecario_biblioteca_citta, bbb.indirizzo bibliotecario_biblioteca_indirizzo
                               FROM Prestiti pr 
                               JOIN Utenti ut on ut.id_utente = pr.id_utente 
                               JOIN Libri li on pr.id_libro = li.id_libro 
                               JOIN Biblioteche bbl on bbl.id_biblioteca = li.id_biblioteca 
                               JOIN Biblioteche bb on bb.id_biblioteca = pr.id_biblioteca
                               JOIN Bibliotecari bi on bi.id_bibliotecario = pr.id_bibliotecario
                               JOIN Biblioteche bbb on bbb.id_biblioteca = bi.id_biblioteca
                               JOIN Categorie ca on ca.id_categoria = li.id_categoria
                               JOIN Generi ge on ge.id_genere = li.id_genere
                               WHERE pr.id_utente = ?""", (id_utente,))
                rows = cursor.fetchall()
                return [self._row_to_prestito(row) for row in rows]
        finally:
            conn.close()

    def _row_to_prestito(self, row: dict) -> Prestito:
        # Per popolare oggetti complessi non è possibile usare
        # return Prestito(**row) if row else None  /  return [Prestito(**row) for row in rows]

        # Utente al quale è stato concesso il Prestito
        utente = Utente(
            id_utente = row['id_utente'],
            nome = row['nome_utente'],
            cognome = row['cognome_utente'],
            email = row['email'],
            telefono = row['telefono']
        )

        # Biblioteca associata al Prestito
        biblioteca = Biblioteca(
            id_biblioteca = row['id_biblioteca'],
            nome_biblioteca = row['nome_biblioteca'],
            citta = row['citta'],
            indirizzo = row['indirizzo']
        )

        # Biblioteca alla quale è assegnato il bibliotecario
        bibliotecario_biblioteca = Biblioteca( 
            id_biblioteca = row['bibliotecario_biblioteca_id_biblioteca'],
            nome_biblioteca = row['bibliotecario_biblioteca_nome_biblioteca'],
            citta = row['bibliotecario_biblioteca_citta'],
            indirizzo = row['bibliotecario_biblioteca_indirizzo']
        )

        # Bibliotecario che ha concesso il Prestito
        bibliotecario = Bibliotecario(
            id_bibliotecario = row['id_bibliotecario'],
            biblioteca = bibliotecario_biblioteca,
            nome = row['nome_bibliotecario'],
            cognome = row['cognome_bibliotecario'],
            email = row['email_bibliotecario'] 
        )

        # Biblioteca alla quale è assegnato il Libro
        libro_biblioteca = Biblioteca(
            id_biblioteca = row['libro_biblioteca_id_biblioteca'],
            nome_biblioteca = row['libro_biblioteca_nome_biblioteca'],
            citta = row['libro_biblioteca_citta'],
            indirizzo = row['libro_biblioteca_indirizzo']
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

        # Libro concesso in Prestito
        libro = Libro(
            id_libro = row['id_libro'],
            biblioteca = libro_biblioteca,
            titolo = row['titolo'],
            autore = row['autore'],
            anno_pubblicazione = row['anno_pubblicazione'],
            isbn = row['isbn'],
            genere = genere,
            categoria = categoria
        )

        # Dati del Prestito
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