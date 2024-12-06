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
        return {}
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
        <button>start competition</button>

            cronometers

        <ul v-for="player in players">

            <Cronometer v-bin:lap="lapsCount", v-bind:player="player"></Cronometer>

        </ul>

        
        

    </div>

</template>