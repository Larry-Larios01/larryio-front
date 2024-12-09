<script lang="ts">

import type { Competition } from "@/models";
import { defineComponent, reactive, toRaw , PropType} from "vue";
import type { Player } from "@/models";


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
    props: {
        players: {
            type: Object as PropType<Player[]>,
            required: true,
        },
        
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
            <div v-for="(player, index) in players" v-bind:key="index">
                <label>
                    <input type="checkbox" >
                </label>
                Player {{ player.name }}
            </div>
        </div>
        <button type="submit">Save</button>
    </form>

</template>