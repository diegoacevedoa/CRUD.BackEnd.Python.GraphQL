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
