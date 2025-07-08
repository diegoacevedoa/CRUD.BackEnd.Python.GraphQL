# CRUD.BackEnd.Python

CRUD de BackEnd en lenguaje de programación Python y base de datos PostgreSQL

PASOS PARA DESARROLLARLO

1- Instalar Python para windows desde la web oficial: https://www.python.org/

2- Crear la carpeta del proyecto y ubicarse en esta en la consola

3- Crear el entorno virtual para que los paquetes instalados no afecten los
   otros proyectos de Python: python -m venv .venv

4- Activamos el entorno virtual en una ventana bash: source .venv/Scripts/activate

5- Instalamos fastapi: pip install "fastapi[standard]"

6- Actualizamos la versión de pip: python -m pip install --upgrade pip

7- Instalamos SQLModel: pip install sqlmodel

8- Instalamos asyncpg: pip install asyncpg

9- Instalamos pydantic-settings: pip install pydantic-settings

10- Instalamos librería de GraphQL: pip install 'strawberry-graphql[fastapi]'

11- Guardamos requerimientos en el archivo requirements.txt: pip freeze > requirements.txt

12- Instalar paquetes desde el archivo requirements.txt (Esto se hace cuando
   no se ha instalado nada, es opcional): pip install -r requirements.txt

13- Crear archivo carpeta src para agregar los archivos del proyecto

14- Crear archivo de inicio del proyecto llamado __init__.py en la carpeta src:

    from fastapi import FastAPI

    app = FastAPI(title="Api Personas", description="A CRUD with Python", openapi_tags=[{"name":"Main", "description": "Main routes" }])

    @app.get("/", tags=["Main"])
    def read_root():
        return {"Hello": "World"}

15- Ejecutamos el proyecto: fastapi dev src/

16- Creamos variable de entorno .env y agregamos la conexión a la base de datos afuera de la carpeta src:

    DATABASE_URL=postgresql+asyncpg://postgres:Medellin1*@localhost:5432/Persona

17- Creamos archivo config.py con el acceso a las variables de entorno del archivo .env en la carpeta src:

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

# print(Config.model_dump())


18- Crear nueva carpeta llamada database en la carpeta src

19- Crear adentro de la carpeta database, el archivo person.py:

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config


class DatabaseSession:
    def __init__(self):
        self.engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))
        self.session_local = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # close connection
    async def close(self):
        await self.engine.dispose()

    # Prepare the context for the asynchronous operation
    async def __aenter__(self) -> AsyncSession:
        self.session = self.session_local()
        return self.session

    # it is used to clean up resources,etc.
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_db(self) -> AsyncSession:
        async with self as db:
            try:
                yield db
            finally:
                db.close()


db = DatabaseSession()



20- Crear nueva carpeta llamada models en la carpeta src

21- Crear adentro de la carpeta models, el archivo person.py:

from sqlmodel import SQLModel, Field


class Person(SQLModel, table=True):
    __tablename__ = "Persona"  # asegura que el nombre coincida con la tabla real
    IdPersona: int | None = Field(default=None, primary_key=True)
    NoDocumento: str = Field(max_length=50)
    Nombres: str = Field(max_length=100)
    Apellidos: str = Field(max_length=100)


22- Crear nueva carpeta llamada schemas en la carpeta src

23- Crear adentro de la carpeta schemas, el archivo person.py:

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



24- Crear nueva carpeta llamada services en la carpeta src

25- Crear adentro de la carpeta services, el archivo person.py:

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



26- Crear nueva carpeta llamada graphql en la carpeta src

27- Crear adentro de la carpeta graphql, el archivo query.py:

from fastapi import Depends
import strawberry
from typing import List
from src.services import person as person_service
from src.schemas.person import PersonType
from graphql import GraphQLError


@strawberry.type
class Query:

    @strawberry.field
    async def get_persons(self) -> List[PersonType]:
        result = await person_service.get_persons()

        return result

    @strawberry.field
    async def get_person(self, id: int) -> PersonType:
        result = await person_service.get_person(id)

        if result:
            return result
        else:
            raise GraphQLError("Data not found", extensions={"error_code": "404"})


28- Crear adentro de la carpeta graphql, el archivo mutation.py:

import strawberry
from src.services import person as person_service
from src.schemas.person import PersonType, PersonInput
from graphql import GraphQLError


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_person(self, data: PersonInput) -> PersonType:
        result = await person_service.create_person(data)
        return result

    @strawberry.mutation
    async def update_person(self, id: int, data: PersonInput) -> PersonType:
        result = await person_service.update_person(id, data)

        if result is None:
            raise GraphQLError("Data not found", extensions={"error_code": "404"})
        else:
            return result

    @strawberry.mutation
    async def delete_person(self, id: int) -> PersonType:
        result = await person_service.delete_person(id)

        if result is None:
            raise GraphQLError("Data not found", extensions={"error_code": "404"})
        else:
            return result


29- Modificamos archivo __init__.py:

from fastapi import FastAPI
import strawberry


from src.graphql.query import Query

from src.graphql.mutation import Mutation
from strawberry.fastapi import GraphQLRouter

app = FastAPI(
    root_path="/api",
    title="Api Personas",
    description="A CRUD with Python",
    openapi_tags=[{"name": "Main", "description": "Main routes"}],
    version="1.0.0",
)

# add graphql endpoint
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/", tags=["Main"])
async def read_root():
    return {"Hello": "World"}


30- Ejecutamos el proyecto: fastapi dev src/
