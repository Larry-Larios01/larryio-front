import { PGlite , MemoryFS} from '@electric-sql/pglite'
//import { PGlite } from "https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js"


interface CompetitionClient  {
    createUser(name: string): Promise<{ id: string; }>
    getUsers(): Promise<{ id: string; name:string }[]>
    createCompetition(name: string, laps: number, players: string[] ): Promise<{ id: string; }>
    getCompetitions(): Promise<{ id: string; name: string, laps:number, players: string[]}[]>
    getUser(id:string): Promise<{ id: string; name: string}>
    insertPodium (id:string, idCompetition: string, place: number): Promise<{id:string}>
    insertPodiumLap(idPlayer:string, idCompetition: string, lap: number, time: number): Promise<{id:string}>


  }
  
  export class CompetitionClientFetch implements CompetitionClient {
  
    async createUser(name: string): Promise<{ id: string; }> {
      // el equivalente a from req
      const req = new Request("http://0.0.0.0:8000/player/" , { method: "POST", headers: { "Content-Type": "application/json" },body: JSON.stringify({ name })});
      const res = await fetch(req)
      // el equivalente a to res en el back
      const data = await res.json()
      return data
    }

    async getUsers(): Promise<{ id: string; name: string}[]> {
        // el equivalente a from req
        const req = new Request("http://0.0.0.0:8000/player/" , { method: "GET", headers: { "Content-Type": "application/json" }});
        const res = await fetch(req)
        console.log("the body is", res.body)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }
    async createCompetition(name: string, laps: number, players: string[] ): Promise<{ id: string; }> {
        // el equivalente a from req
        const req = new Request("http://0.0.0.0:8000/competition/" , { method: "POST", headers: { "Content-Type": "application/json" },body: JSON.stringify({ 
          name: name,
          laps: laps,
          players: players})});
        const res = await fetch(req)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }
      async getCompetitions(): Promise<{ id: string; name: string, laps:number, players: string[]}[]> {
        // el equivalente a from req
        const req = new Request("http://0.0.0.0:8000/competition/" , { method: "GET", headers: { "Content-Type": "application/json" }});
        const res = await fetch(req)
        console.log("the body is", res.body)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }

      async getUser(id:string): Promise<{ id: string; name: string}> {
        // el equivalente a from req
        const req = new Request(`http://0.0.0.0:8000/player/${id}` , { method: "GET", headers: { "Content-Type": "application/json" }});
        const res = await fetch(req)
        console.log("the body of get  is", res.body)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }

      async insertPodium (idPlayer:string, idCompetition: string, place: number): Promise<{id:string}>{

        const req = new Request("http://0.0.0.0:8000/podium/" , { method: "POST", headers: { "Content-Type": "application/json" },body: JSON.stringify({ 
          idPlayer: idPlayer,
          idCompetition: idCompetition,
          place: place})});
        const res = await fetch(req)
        console.log("the body of get  is", res.body)
        // el equivalente a to res en el back
        const data = await res.json()
        return data

      }
      async getPodiums(): Promise<{ id_player: string; name: string; place1: number, place2:number, place3: number}[]> {
        // el equivalente a from req
        const req = new Request("http://0.0.0.0:8000/podium/" , { method: "GET", headers: { "Content-Type": "application/json" }});
        const res = await fetch(req)
        console.log("the body is in podiums", res.body)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }

      async insertPodiumLap(idPlayer:string, idCompetition: string, lap: number, time: number): Promise<{id:string}>{
        const req = new Request("http://0.0.0.0:8000/podium_lap/" , { method: "POST", headers: { "Content-Type": "application/json" },body: JSON.stringify({ 
          idPlayer: idPlayer,
          idCompetition: idCompetition,
          lap: lap ,
          time: time})});
        const res = await fetch(req)
        console.log("the body of post lap is", res.text)
        // el equivalente a to res en el back
        const data = await res.json()
        return data


      }




    
  }


  export class CompetitionClientPg implements CompetitionClient {

    async createConnection(): Promise<PGlite>{

        const db = new PGlite({
          fs: new MemoryFS(),
        })

        await db.exec(`
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS competition (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT
);

CREATE TABLE IF NOT EXISTS competition_master (
  id_player UUID NOT NULL,
  id_competition UUID NOT NULL,
  place INT,
  PRIMARY KEY (id_player, id_competition),
  FOREIGN KEY (id_player) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (id_competition) REFERENCES competition (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS podium_detail (
  id_player UUID NOT NULL,
  id_competition UUID NOT NULL,
  lap INT,
  time INT,
  PRIMARY KEY (id_player, id_competition, lap),
  FOREIGN KEY (id_player) REFERENCES users (id) ON DELETE CASCADE,
  FOREIGN KEY (id_competition) REFERENCES competition (id) ON DELETE CASCADE
);`)

        return db 


    }

    async createUser(name: string): Promise<{ id: string; }> {
     const  db = await this.createConnection()
    const query = `INSERT INTO players (name) VALUES ($1) RETURNING id;`;
    const result = await db.query(query, [name]);
       return { id: result.rows[0].id };
    }







  }


  


