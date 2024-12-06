<script lang="ts">

import { defineComponent, ref } from "vue"
import type { PropType } from "vue";
import type { Player } from "@/models";
import Cronometer from "./Cronometer.vue";



export default defineComponent({
    name: "Competition",
    components: {
    Cronometer
  },
    props: {
        players: {
            type: Object as PropType<Player[]>,
            required: true,
        },
        lapsCount: {
            type: Number,
            required: true
        }
    },
    setup(props, ctx) {
        let competitionStarted : boolean = ref(false);

        function startCompetition(){
            competitionStarted.value = true

        }
        return { competitionStarted, startCompetition}
    }
})

</script>

<template>

    <div>
        Players:
        <ul v-for="player in players">
            <li>{{ player.name }}</li>
        </ul>
    </div>
    <div>
        Laps: {{ lapsCount }}
    </div>


    <div>
        <button v-on:click="startCompetition()">start competition</button>

        <div v-if="competitionStarted">

            <ul v-for="(player, index) in players">
                <label>{{ player.name }}


                    <Cronometer v-bin:laps="lapsCount" v-bind:player="player.name"></Cronometer>
                </label>

                

            </ul>



        </div>

       
        
        

    </div>

</template>