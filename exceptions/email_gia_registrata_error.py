class EmailGiaRegistrataError(Exception):

    def __init__(self, email: str) -> None:
        super().__init__(f"L'email '{email}' è già registrata.")
        self.email = email
