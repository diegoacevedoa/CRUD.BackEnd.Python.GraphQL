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
