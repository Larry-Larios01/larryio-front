export type Player = {
    name: string
}

export type Competition = {
    name: string
    lapsCount: number
    players: Player[]
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