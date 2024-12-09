<script lang="ts">

import type { Competition } from "@/models";
import { defineComponent, reactive, toRaw , PropType, ref} from "vue";
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
            type: Array as PropType<Player[]>,
            required: true,
        },
        
    },
    setup(props, ctx) {
        const competition = reactive<Competition>({
            name: "",
            lapsCount: 0,
            players: []
        })

        const checkedNames = ref<string[]>([]); 
        function addPlayer() {
            competition.players.push({ name: "", podium: { place1: 0, place2: 0, place3: 0 },})
        }
        console.log(props.players)

        function save() {
            const payload = toRaw(competition)
            ctx.emit("register", payload)
        }

        return {
            competition,
            addPlayer,
            save,
            checkedNames
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


        <div v-for="player in players">
            <input type="checkbox" v-bind:value="player.name" v-bind:id="player.name" v-model="checkedNames">
            <label >{{ player.name }}</label>
        </div>
        <button type="submit">Save</button>
    </form>

</template>