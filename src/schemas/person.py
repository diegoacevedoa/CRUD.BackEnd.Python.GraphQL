import strawberry


@strawberry.type
class PersonType:
    id_persona: int
    no_documento: str
    nombres: str
    apellidos: str


@strawberry.input
class PersonInput:
    no_documento: str
    nombres: str
    apellidos: str
