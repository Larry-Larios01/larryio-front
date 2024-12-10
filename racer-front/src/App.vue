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
    const listCompetition = ref<CompetitionT[]>([]);
    const playersRegistered = ref<Player[]>([]);
    const isVisiblecompetitionRegistration = ref(false);
    const startCareer = ref(false);
    function register(competion: CompetitionT) {
      currentCompetition.value = competion
      listCompetition.value.push(currentCompetition.value)
      isVisiblecompetitionRegistration.value = false
    }

    function startCareerbtn(){
      startCareer.value = true

    }

    function registerPlayer(players: Player[]){
      playersRegistered.value = players
    }

    function createNewCompettiionregistration(){
      isVisiblecompetitionRegistration.value = true
    }

    return {
      hello,
      register,
      currentCompetition,
      registerPlayer,
      playersRegistered,
      isVisiblecompetitionRegistration,
      createNewCompettiionregistration,
      listCompetition,
      startCareer,
      startCareerbtn
    }
  }
})
</script>

<template>
  <header>
  </header>

  <main>
    <div>Hello {{ hello }}</div>

    <PlayerRegistration v-on:registered="registerPlayer"> </PlayerRegistration>


    <button v-on:click="createNewCompettiionregistration">add new competition</button>
    <CompetitionRegistration v-if="isVisiblecompetitionRegistration " v-on:register="register" v-bind:players="playersRegistered"  >
    </CompetitionRegistration>


    <button v-on:click="startCareerbtn">start career</button>

    <div v-for="current in listCompetition">
      <Competition v-if="startCareer" v-bind:laps-count="current.lapsCount"
      v-bind:players="current.players"></Competition>
    </div>

   
  </main>
</template>

<style scoped></style>
