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
    const isVisibleRegisterplayer = ref(false);
    const isVisiblestartCompetition = ref(false);
    const startCareer = ref(false);
    function register(competion: CompetitionT) {
      currentCompetition.value = competion
      listCompetition.value.push(currentCompetition.value)
      isVisiblecompetitionRegistration.value = false
      isVisiblestartCompetition.value = true
    }

    function startCareerbtn(){
      startCareer.value = true

    }

    function registerPlayer(players: Player[]){
      playersRegistered.value = players;
      isVisibleRegisterplayer.value= false;
      isVisiblecompetitionRegistration.value = true;
    }

    function createNewCompettiionregistration(){
      isVisiblecompetitionRegistration.value = true;
    }

    function showCreateplayer(){
      isVisibleRegisterplayer.value = true;
      isVisiblecompetitionRegistration.value = false;
      isVisiblestartCompetition.value = false
    }

    function showCreatecompetition(){
      isVisibleRegisterplayer.value = false;
      isVisiblecompetitionRegistration.value = true;
      isVisiblestartCompetition.value = false
    }
    function showStartcompetition(){
      isVisibleRegisterplayer.value = false;
      isVisiblecompetitionRegistration.value = false;
      isVisiblestartCompetition.value = true
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
      podiumPlayers,
      isVisibleRegisterplayer,
      isVisiblestartCompetition,
      showCreateplayer,
      showCreatecompetition,
      showStartcompetition
    }
  }
})
</script>

<template>
<div class="principal">
  <header>
      <div class="top-of-header">
        <p>Racer App</p>
      </div>
      <div class="bottom-of-header">
        <button v-on:click="showCreateplayer">create player</button>
        <button v-on:click="showCreatecompetition">create competition</button>
        <button v-on:click="showStartcompetition">start career </button>
      </div>
  </header>

  <main>
    

    <PlayerRegistration v-on:registered="registerPlayer" v-if="isVisibleRegisterplayer"> </PlayerRegistration>


    
    <CompetitionRegistration v-if="isVisiblecompetitionRegistration " v-on:register="register" v-bind:players="playersRegistered"  >
    </CompetitionRegistration>


  

    <div v-for="current in listCompetition">
      <Competition v-if="isVisiblestartCompetition" v-bind:laps-count="current.lapsCount"
      v-bind:players="current.players" v-on:podiumFinal="podiumFinal"></Competition>
    </div>

    
    
   
  </main>

  <div class="global-podium">
      <p>Global podium</p>
      <div v-for="pplayer in podiumPlayers">
    {{ pplayer.name }} 
    first place={{ pplayer.podium.place1 }}

    second place={{ pplayer.podium.place2 }}

    third place ={{ pplayer.podium.place3 }}


   </div>


    </div>

    
</div>
  
</template>

<style scoped>
.principal{
  height: 100vh;
  width: 100vw;
  display: grid;
  grid-template-rows: 100px 1fr 194px;
  grid-template-columns: 1fr 270px  ;
}
header{
  display: grid;
  grid-row-start: 1;
  grid-row-end: 1;
  grid-column-start: 1;
  grid-column-end: 3;
  grid-template-rows: 40px 60px;
  grid-template-columns: 250px 1333px;
  background-color: #0A0A0A;
  color: #FFFFFF;

}
.top-of-header{
  grid-row-start: 1;
  grid-column-start: 2;
  display: flex;
  justify-content: center;
}
.bottom-of-header {
display: flex;
align-items: flex-end;
justify-content: center;
font-size: 15px;
margin: 20px;
grid-row-start: 2;
grid-column-start: 2;
}


.bottom-of-header button{
  text-decoration: none;
  margin: 0 10px;
  color: #FFFFFF;
  border: 0;
  background-color: #0A0A0A;
}

.bottom-of-header button:hover {
      background-color: #0056b3;
      color: #ffdd00;
      transform: scale(1.1); 
    }

  .global-podium{
   grid-column-start: 2;
   grid-row-start: 2;
  }


</style>
