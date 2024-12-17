from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from dotenv import load_dotenv
import uuid
import json
from pydantic import BaseModel, UUID4
import os
import uvicorn
from starlette.requests import Request
import psycopg
from psycopg.rows import dict_row
from psycopg import AsyncRawCursor



load_dotenv(verbose=True)
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)

async def get_connection():
    return await psycopg.AsyncConnection.connect(DATABASE_URL, row_factory=dict_row, cursor_factory= AsyncRawCursor)





class User(BaseModel):
    id: UUID4
    name:str

async def from_req_insert_user(request: Request)-> User:
    uuid4 = uuid.uuid4()
    data =  await request.json()
    print(data)
    contact = User(id=uuid4,name=data["name"])
    return contact

async def insert_user_handler(params: User, conn)-> uuid:
   
    async with conn.cursor() as c:
            result = await c.execute(
                "INSERT INTO users (id, name) VALUES ($1, $2) RETURNING id, name",
                [params.id, params.name]
                    )
            user = await result.fetchone()
            print(user)
            user_created = User(id=user["id"],name=user['name'])
    await conn.commit()
    print(user_created.name)
            
    return user_created


def to_res_insert_user(user: User)-> JSONResponse:
     return JSONResponse({
        "id": f"{user.id}",
        "message": "was succesful inserted"
    })

async def insert_user(request: Request):
    params =  await from_req_insert_user(request)
    conn = await get_connection()
    result = await insert_user_handler(params, conn)
    return to_res_insert_user(result)



async def get_users_handler(conn)-> User:
    players: list[User] = []
    conn = await get_connection()
    async with conn.transaction():
            restult = await conn.execute("SELECT * FROM users")
            users = await restult.fetchall()
            for user in users:
                player = User(id=user["id"],name=user["name"])
                players.append(player)


                  
           
    await conn.close()
    return players


def to_res_get_users(users: list[User])-> JSONResponse:
     user_serialized = [user.model_dump_json(indent=2) for user in users]
     print(user_serialized)
     return JSONResponse(user_serialized)



async def get_users(request: Request):
    conn = await get_connection()
    
    result = await get_users_handler(conn)
    return to_res_get_users(result)

        




routes = [
    Route("/Player/", endpoint=insert_user, methods=["POST"]),
    Route("/Player/", endpoint=get_users, methods=["GET"])
]



app = Starlette(
    routes=routes
)



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)