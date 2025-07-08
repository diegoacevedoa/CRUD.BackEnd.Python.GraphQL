from sqlmodel import select
from src.schemas.person import PersonInput, PersonType
from src.models.person import Person
from src.database.person import db


async def get_persons():
    async with db as session:
        statement = select(Person)

        result = await session.exec(statement)

        list_data = result.all()

    return [
        PersonType(
            id_persona=data.IdPersona,
            no_documento=data.NoDocumento,
            nombres=data.Nombres,
            apellidos=data.Apellidos,
        )
        for data in list_data
    ]


async def get_person(id: int):
    async with db as session:
        statement = select(Person).where(Person.IdPersona == id)

        result = await session.exec(statement)

        data = result.first()

    return (
        PersonType(
            id_persona=data.IdPersona,
            no_documento=data.NoDocumento,
            nombres=data.Nombres,
            apellidos=data.Apellidos,
        )
        if data is not None
        else None
    )


async def create_person(data: PersonInput):
    async with db as session:
        new_data = Person()
        new_data.NoDocumento = data.no_documento
        new_data.Nombres = data.nombres
        new_data.Apellidos = data.apellidos

        session.add(new_data)

        await session.commit()

    return PersonType(
        id_persona=new_data.IdPersona,
        no_documento=new_data.NoDocumento,
        nombres=new_data.Nombres,
        apellidos=new_data.Apellidos,
    )


async def update_person(id: int, data: PersonInput):
    async with db as session:
        statement = select(Person).where(Person.IdPersona == id)

        result = await session.exec(statement)

        data_to_update = result.first()

        if data_to_update is not None:
            data_to_update.NoDocumento = data.no_documento
            data_to_update.Nombres = data.nombres
            data_to_update.Apellidos = data.apellidos

            session.add(data_to_update)

            await session.commit()

            await session.refresh(data_to_update)

            return PersonType(
                id_persona=data_to_update.IdPersona,
                no_documento=data_to_update.NoDocumento,
                nombres=data_to_update.Nombres,
                apellidos=data_to_update.Apellidos,
            )
        else:
            return None


async def delete_person(id: int):
    async with db as session:
        statement = select(Person).where(Person.IdPersona == id)

        result = await session.exec(statement)

        data_to_delete = result.first()

        if data_to_delete is not None:
            await session.delete(data_to_delete)

            await session.commit()

            return PersonType(
                id_persona=data_to_delete.IdPersona,
                no_documento=data_to_delete.NoDocumento,
                nombres=data_to_delete.Nombres,
                apellidos=data_to_delete.Apellidos,
            )
        else:
            return None
