<script lang="ts">

import { defineComponent, ref, toRaw } from "vue"
import type { PropType } from "vue";
import type { Player, Results } from "@/models";
import Cronometer from "./Cronometer.vue";
import { Key } from "readline";
import { EmitFlags } from "typescript";



export default defineComponent({
    name: "Competition",
    components: {
    Cronometer
  },
  emits: {
  podiumFinal(payload: Results[]) {
    return Array.isArray(payload) &&
      payload.every(result => 
        typeof result === "object" &&
        typeof result.player === "object" &&
        typeof result.player.name === "string" &&
        Array.isArray(result.laps) &&
        result.laps.every(lap => typeof lap === "number")
      );
  }
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
        const  competitionStarted : boolean = ref(false);
        const results = ref<Results[]>([]);
        function startCompetition(){
            competitionStarted.value = true

        }

        function handlerFinished(resultt: Results){

            results.value.push(resultt)

            console.log(results.value.length)
            if(results.value.length == 3){
                const payload = toRaw(results.value)
                console.log(payload)
    
                ctx.emit('podiumFinal', payload)
            }

        }
        return { competitionStarted, startCompetition, handlerFinished, results}
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

            <ul v-for="(player, index) in players ">
                <label>{{ player.name }}


                    <Cronometer v-bind:laps="lapsCount" v-bind:player="player"  v-on:finished="handlerFinished"></Cronometer>
                </label>

                

            </ul>



        </div>
        podium:

        <ul v-for="result in results"> {{ result.player.name}}</ul>
        
        

    </div>

</template>