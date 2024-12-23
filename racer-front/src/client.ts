

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


