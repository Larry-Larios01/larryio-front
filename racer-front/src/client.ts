interface CompetitionClient  {
    createUser(name: string): Promise<{ id: string; }>
    getUsers(): Promise<{ id: string; name:string }[]>

  }
  
  export class CompetitionClientFetch implements CompetitionClient {
  
    async createUser(name: string): Promise<{ id: string; }> {
      // el equivalente a from req
      const req = new Request("http://0.0.0.0:8000/Player/" , { method: "POST", headers: { "Content-Type": "application/json" },body: JSON.stringify({ name })});
      const res = await fetch(req)
      // el equivalente a to res en el back
      const data = await res.json()
      return data
    }

    async getUsers(): Promise<{ id: string; name: string}[]> {
        // el equivalente a from req
        const req = new Request("http://0.0.0.0:8000/Player/" , { method: "GET", headers: { "Content-Type": "application/json" }});
        const res = await fetch(req)
        // el equivalente a to res en el back
        const data = await res.json()
        return data
      }
  }


