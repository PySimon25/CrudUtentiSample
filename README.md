# Gestione Utenti – Progetto Python con architettura a layer

Questo progetto è un esempio di **applicazione Python organizzata in modo modulare**, secondo l'architettura a strati (DTO, Repository/DAO, Service). Utilizza un database **MariaDB** per la gestione degli utenti.

## Funzionalità principali

- **CRUD utenti** (Create, Read, Update, Delete)
- **Accesso ai dati tramite interfacce DAO**
- **Business logic isolata nei service**
- **Salvataggio dei record su MariaDB**

## Setup progetto

- Installazione pacchetti

    ``` bash
    pip install -r requirements.txt
    ```

- Creazione della tabella sul database

    ``` sql
    CREATE TABLE `Utenti` (
    `id_utente` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `nome` varchar(100) DEFAULT NULL,
    `cognome` varchar(100) DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL,
    `telefono` varchar(15) DEFAULT NULL,
    PRIMARY KEY (`id_utente`),
    UNIQUE KEY `uni_email` (`email`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ```

- Copia o rinomina file **.env.dist** in **.env** e compilazione con i dati corretti per il database in uso

- Esecuzione del progetto con

    ``` bash
    python main.py
    ```

- Tecnologie usate

    Python 3.10+  
    MariaDB  
    PEP 8 / typing / dataclass  
    Architettura a strati (DTO / DAO / Service)  
    Connection Pool MariaDB
