<script lang="ts">
import { defineComponent, ref } from "vue"
import Competition from "./components/Competition.vue"
import type { Player } from "./components/Competition.vue";

export default defineComponent({
  name: "App",
  components: {
    Competition
  },
  setup() {
    const hello = ref("world")
    const players = ref<Player[]>([{
      name: "Larry"
    }, {
      name: "Gerson"
    }])

    return {
      hello,
      players,
    }
  }
})
</script>

<template>
  <header>
  </header>

  <main>
    <div>Hello {{ hello }}</div>
    <Competition v-bind:laps-count="6" v-bind:players="players"></Competition>
  </main>
</template>

<style scoped></style>
