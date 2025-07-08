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
