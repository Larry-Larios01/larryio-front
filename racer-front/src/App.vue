<script lang="ts">
import { defineComponent, ref } from "vue"
import Competition from "./components/Competition.vue"
import CompetitionRegistration from "./components/CompetitionRegistration.vue";
import type { Competition as CompetitionT, Player, Results, PodiumPLayer } from "./models";
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
    const podiumPlayers = ref<PodiumPLayer[]>([]);



    const results = ref<Results[]>([]);
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


    function podiumFinal(podium: Results[]) {
      results.value = podium;

      results.value.forEach((player, index) => {
        const existingPlayer = podiumPlayers.value.find(
          (podiumPlayer) => podiumPlayer.name === player.player.name
        );

        if (!existingPlayer) {
          const newPodium = {
            name: player.player.name,
            podium: {
              place1: index === 0 ? 1 : 0,
              place2: index === 1 ? 1 : 0,
              place3: index === 2 ? 1 : 0,
            },
          };
          podiumPlayers.value.push(newPodium);
        } else {
          if (index === 0) existingPlayer.podium.place1 += 1;
          if (index === 1) existingPlayer.podium.place2 += 1;
          if (index === 2) existingPlayer.podium.place3 += 1;
        }
      });

      console.log("Updated podium players:", podiumPlayers.value);
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
      startCareerbtn,
      podiumFinal,
      podiumPlayers
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
      v-bind:players="current.players" v-on:podiumFinal="podiumFinal"></Competition>
    </div>
    Podium Global
   <div v-for="pplayer in podiumPlayers">
    {{ pplayer }} 


   </div>
  </main>
</template>

<style scoped></style>
