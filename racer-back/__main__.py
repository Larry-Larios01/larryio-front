from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from dotenv import load_dotenv
import uuid
from pydantic import BaseModel, UUID4
import os
import uvicorn
from starlette.requests import Request
import psycopg
from psycopg.rows import dict_row
from psycopg import AsyncRawCursor
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


load_dotenv(verbose=True)
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)

async def get_connection():
    return await psycopg.AsyncConnection.connect(DATABASE_URL, row_factory=dict_row, cursor_factory= AsyncRawCursor)





class User(BaseModel):
    id: UUID4
    name:str

class Competition(BaseModel):
    id: UUID4
    name: str
    laps: int
    players: list[UUID4]

class Podium(BaseModel):
    id_competition: UUID4
    id_player: UUID4
    place: int


class PlayerPodium(BaseModel):
    id_player: UUID4
    name: str
    place1: int
    place2: int 
    place3: int

class PlayerPodiumLap(BaseModel):
    id_player: UUID4
    id_competition: str
    lap: int
    time: int 
    
     



    #the start of the logic of the endpoit insert a user(player)

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



    #the start of the logic of the endpoit getusers


async def get_users_handler(conn)-> User:
    players: list[User] = []
    async with conn.transaction():
            restult = await conn.execute("SELECT * FROM users")
            users = await restult.fetchall()
            for user in users:
                player = User(id=user["id"],name=user["name"])
                players.append(player)      
    await conn.close()
    return players


def to_res_get_users(users: list[User])-> JSONResponse:
     user_serialized = [user.model_dump(mode="json") for user in users]
     print(user_serialized)
     return JSONResponse(user_serialized)



async def get_users(request: Request):
    conn = await get_connection()
    result = await get_users_handler(conn)
    return to_res_get_users(result)



    #the start of the logic of the endpoit insert a competition



async def from_req_insert_competition(request: Request)-> Competition:
    uuid4 = uuid.uuid4()
    data =  await request.json()
    players = [uuid.UUID(player) for player in data["players"]]
    print(players)
    competition = Competition(id=uuid4,name=data["name"], players=players, laps=data["laps"] )
    return competition

async def insert_competition_handler(params: Competition, conn)-> uuid:
   
    async with conn.cursor() as c:
            result = await c.execute(
                "INSERT INTO competition (id, name, laps) VALUES ($1, $2, $3) RETURNING id, name, laps",
                [params.id, params.name, params.laps]
                    )
            comp = await result.fetchone()
            print(comp)
            competition = Competition(id=comp["id"],name=comp['name'], players=params.players, laps=comp["laps"])

            for user in params.players:
                  await c.execute(
                "INSERT INTO competition_master (id_player, id_competition) VALUES ($1, $2) ",
                [user, competition.id]
                    )
            
    await conn.commit()
            
    return competition.id


def to_res_insert_competition(comp_id: uuid)-> JSONResponse:
     return JSONResponse({
        "id": f"{comp_id}",
        "message": "was succesful inserted"
    })

async def insert_competition(request: Request):
    params =  await from_req_insert_competition(request)
    conn = await get_connection()
    result = await insert_competition_handler(params, conn)
    return to_res_insert_competition(result)



    #the start of the logic of the endpoit getthecompetitions

async def get_competitions_handler(conn)-> list[Competition]:
    competitions: list[Competition] = []
    async with conn.transaction():
            restult = await conn.execute("SELECT * FROM competition")
            comps = await restult.fetchall()
            for comp in comps:
                players = await conn.execute("SELECT cm.id_player FROM competition c INNER JOIN competition_master cm ON c.id = cm.id_competition WHERE c.id = $1;", [comp["id"]])
                players_get = await players.fetchall()
                players_send = [row["id_player"] for row in players_get]
                competition = Competition(id=comp["id"],name=comp["name"], players=players_send, laps=comp["laps"])
                competitions.append(competition)      
    await conn.close()
    return competitions


def to_res_get_competitions(comps: list[Competition])-> JSONResponse:
     user_serialized = [comp.model_dump(mode="json") for comp in comps]
     print(user_serialized)
     return JSONResponse(user_serialized)



async def get_competitions(request: Request):
    conn = await get_connection()
    result = await get_competitions_handler(conn)
    return to_res_get_competitions(result)


#the begin of the logic to get one user
def from_req_get_user(request: Request)-> uuid.UUID:
    user_id = request.path_params.get("id")
    uuid_obj = uuid.UUID(user_id)
    print("the id of param",uuid_obj)
    return uuid_obj


async def get_user_handler(params: uuid.UUID, conn)-> User:
    async with conn.transaction():
            restult = await conn.execute("SELECT * FROM users WHERE id = $1",[params])
            user = await restult.fetchone()
            contact = User(id=user["id"],name=user["name"])
    await conn.close()
    return contact


def to_res_get_user(player: User)-> JSONResponse:
     user_serialized = player.model_dump(mode="json")
     return JSONResponse(user_serialized)



async def get_user(request: Request):
    conn = await get_connection()
    params = from_req_get_user(request)
    result = await get_user_handler(params, conn)
    return to_res_get_user(result)


#the logic of insert a new podium of a specific career 
async def from_req_insert_podium(request: Request)-> Podium:
    data =  await request.json()
    print("the data of the request of insert podium is", data)
    id_player_uuid = uuid.UUID(data["idPlayer"])
    id_comp_uuid = uuid.UUID(data["idCompetition"])
    place = int(data["place"])
    podium = Podium(id_competition=id_comp_uuid, id_player=id_player_uuid, place=place)
    return podium

async def insert_podium_handler(params: Podium, conn)-> uuid:
   
    async with conn.cursor() as c:
            result = await c.execute(
                "UPDATE competition_master SET place = $1 WHERE id_player = $2 AND id_competition = $3;",
                [params.place, params.id_player, params.id_competition]
                    )
    await conn.commit()
    
            
    return params.id_player


def to_res_insert_podium(user: uuid)-> JSONResponse:
     return JSONResponse({
        "id": f"{user}",
        "message": "was succesful in the podium"
    })

async def insert_podium(request: Request):
    params =  await from_req_insert_podium(request)
    conn = await get_connection()
    result = await insert_podium_handler(params, conn)
    return to_res_insert_podium(result)


# the logic to get the all podiums
async def get_podiums_handler(conn)-> list[PlayerPodium]:
    podiums_player: list[PlayerPodium] = []
    async with conn.transaction():
            query = """  SELECT u."id", u."name",
           COUNT(CASE WHEN place = 1 THEN 1 END) AS first_place,
           COUNT(CASE WHEN place = 2 THEN 1 END) AS second_place,
           COUNT(CASE WHEN place = 3 THEN 1 END) AS third_place
        FROM competition_master c
        INNER JOIN users u ON u.id = c.id_player
        GROUP BY u."name", u."id";"""
            restult = await conn.execute(query)
            podium = await restult.fetchall()
            for pod in podium:

                podium_player = PlayerPodium(id_player=pod["id"], name=pod["name"], place1=pod["first_place"], place2=pod["second_place"], place3=pod["third_place"])
                podiums_player.append(podium_player)      
    await conn.close()
    return podiums_player


def to_res_get_podiums(pods: list[PlayerPodium])-> JSONResponse:
     pods_serialized = [pod.model_dump(mode="json") for pod in pods]
     print("the spected body", pods_serialized)
     return JSONResponse(pods_serialized)



async def get_podiums(request: Request):
    conn = await get_connection()
    result = await get_podiums_handler(conn)
    return to_res_get_podiums(result)


#the logic of insert a new podium of a specific lap
async def from_req_insert_lap(request: Request)-> PlayerPodiumLap:
    data =  await request.json()
    podium_lap = PlayerPodiumLap(id_competition=data["idCompetition"], id_player=data["idPlayer"], lap=data["lap"], time=data["time"])
    return podium_lap

async def insert_lap_handler(params: PlayerPodiumLap, conn)-> uuid:
   
    async with conn.cursor() as c:
            result = await c.execute(
                "INSERT INTO podium_detail (id_player, id_competition, lap, time) VALUES ($1, $2, $3, $4)",
                [params.id_player, params.id_competition, params.lap, params.time]
                    )
    await conn.commit()
    
            
    return params.id_player


def to_res_insert_lap(user: uuid)-> JSONResponse:
     return JSONResponse({
        "id": f"{user}",
        "message": "was succesful in the podium"
    })

async def insert_lap(request: Request):
    params =  await from_req_insert_lap(request)
    conn = await get_connection()
    result = await insert_lap_handler(params, conn)
    return to_res_insert_lap(result)

        




routes = [
    Route("/player/", endpoint=insert_user, methods=["POST"]),
    Route("/player/", endpoint=get_users, methods=["GET"]),
    Route("/player/{id}", endpoint=get_user, methods=["GET"]),
    Route("/competition/", endpoint=insert_competition, methods=["POST"]),
    Route("/competition/", endpoint=get_competitions, methods=["GET"]),
    Route("/podium/", endpoint=insert_podium, methods=["POST"]),
    Route("/podium/", endpoint=get_podiums, methods=["GET"]),
    Route("/podium_lap/", endpoint=insert_lap, methods=["POST"]),
]


middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["*"],  allow_headers=["*"])
]



app = Starlette(
    routes=routes,
    middleware=middleware
)




if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)