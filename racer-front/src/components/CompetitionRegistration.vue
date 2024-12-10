<script lang="ts">

import type { Competition } from "@/models";
import { defineComponent, reactive, toRaw , PropType, ref, onMounted} from "vue";
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

         console.log("Players received in CompetitionRegistration:", props.players);
        const competition = reactive<Competition>({
            name: "",
            lapsCount: 0,
            players: []
        })

        
        const checkedNames = ref<Player>({ name: "" });
        const playersT = ref<Player[]>([]);

        function save() {
            competition.players = playersT.value
            const payload = toRaw(competition)
            ctx.emit("register", payload)
        };
        function addPlayer(){
            playersT.value.push(checkedNames.value)
            checkedNames.value = {name: ""}

        }

    

        return {
            competition,
            save,
            checkedNames, 
            addPlayer
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
            <select v-model="checkedNames">
            <option v-for="player in players" v-bind:value="player">
             {{ player.name}}
            </option>
            </select>

        </div>
        
    
        <button type="submit">Save</button>
        <button  v-on:click="addPlayer">addPlayer</button>
    </form>

</template>