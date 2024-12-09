<script lang="ts">
import { defineComponent, ref } from "vue"
import Competition from "./components/Competition.vue"
import CompetitionRegistration from "./components/CompetitionRegistration.vue";
import type { Competition as CompetitionT, Player } from "./models";
import PlayerRegistration from "./components/PlayerRegistration.vue";
export default defineComponent({
  name: "App",
  components: {
    Competition,
    CompetitionRegistration,
    PlayerRegistration
  },
  setup() {
    const hello = ref("world")
    const currentCompetition = ref<CompetitionT>()
    function register(competion: CompetitionT) {
      currentCompetition.value = competion
    }

    return {
      hello,
      register,
      currentCompetition
    }
  }
})
</script>

<template>
  <header>
  </header>

  <main>
    <div>Hello {{ hello }}</div>
    <PlayerRegistration> </PlayerRegistration>
    <CompetitionRegistration v-if="!currentCompetition" v-on:register="register">
    </CompetitionRegistration>

    <Competition v-if="currentCompetition" v-bind:laps-count="currentCompetition.lapsCount"
      v-bind:players="currentCompetition.players"></Competition>
  </main>
</template>

<style scoped></style>
