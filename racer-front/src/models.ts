export type Player = {
    id: string
    name: string
}


export type PodiumPLayer = {
    id: string 
    name: string
    place1: number
    place2: number
    place3: number
}


export type Animal = {
    id: string
    name: String
}


export type PodiumPlayerLap = {
    idCompetition: string 
    idPlayer : string
    playerName: string
    
}

export type PlayerFinished = {
    idPlayer: string
    idCompetition: string
    place: number 
}



export type Competition = {
    name: string
    lapsCount: number
    players: string[]
}

export type CompetitionStarted = {
    id: string
    name: string
    lapsCount: number
    players: string[]
}

export type CompetitonCompleted = {
    podium: Player[]
    laps: Record<string, number>[]
}

const larry = {
    name: "larry"
} satisfies Player

const gerson = {
    name: "gerson"
} satisfies Player

const value = {
    podium: [gerson, larry],
    laps: [
        {
            "larry": 10,
            "gerson": 20
        }
    ]
} satisfies CompetitonCompleted


export type Results = {
    player: Player,
    laps: number[]
}