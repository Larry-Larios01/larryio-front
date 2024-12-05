<script lang="ts">

import { defineComponent, ref } from "vue"
import type { PropType } from "vue";

export type Player = {
    name: string
}

export default defineComponent({
    name: "Competition",
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

</template>