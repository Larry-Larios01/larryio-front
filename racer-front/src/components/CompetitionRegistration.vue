<script lang="ts">

import type { Competition } from "@/models";
import { defineComponent, reactive, toRaw } from "vue";


export default defineComponent({
    name: "CompetitionRegistration",
    emits: {
        register(payload: Competition) {
            return typeof payload === "object" &&
                typeof payload.name === "string" &&
                typeof payload.lapsCount === "number" &&
                Array.isArray(payload.players) &&
                payload.players.every(player => typeof player.name === "string")
        }
    },
    setup(props, ctx) {
        const competition = reactive<Competition>({
            name: "",
            lapsCount: 0,
            players: []
        })
        function addPlayer() {
            competition.players.push({ name: "" })
        }

        function save() {
            const payload = toRaw(competition)
            ctx.emit("register", payload)
        }

        return {
            competition,
            addPlayer,
            save
        }
    }
})

</script>

<template>
    <form v-on:submit.prevent="save">

        <div>
            <label>Name:
                <input type="text" v-model="competition.name">
            </label>
        </div>
        <div>

            <label>Laps:
                <input type="number" name="laps" v-model="competition.lapsCount">
            </label>
        </div>


        <div>
            <div v-for="(player, index) in competition.players" v-bind:key="index">
                <label>Player {{ index + 1 }}
                    <input type="text" v-model="player.name">
                </label>
            </div>
            <button type="button" v-on:click="addPlayer">Add Player</button>
        </div>
        <button type="submit">Save</button>
    </form>

</template>