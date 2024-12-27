<script lang="ts">
import { defineComponent, ref, onMounted } from "vue"
import Competition from "./components/Competition.vue"
import CompetitionRegistration from "./components/CompetitionRegistration.vue";
import type { Competition as CompetitionT, Player, Results, PodiumPLayer, CompetitionStarted, Animal } from "./models";
import PlayerRegistration from "./components/PlayerRegistration.vue";
import {CompetitionClientFetch} from '@/client'
import  Select2Component from "@/components/Select2.vue";
export default defineComponent({
  name: "App",
  components: {
    Competition,
    CompetitionRegistration,
    PlayerRegistration,
    Select2Component
  },
  setup() {
    const hello = ref("world")
    const currentCompetition = ref<CompetitionT>()
    const listCompetition = ref<CompetitionT[]>([]);
    const playersRegistered = ref<Player[]>([]);
    const podiumPlayers = ref<PodiumPLayer[]>([]);
    const comps = ref<CompetitionStarted[]>([]);
    const nameSelect = ref("maicol")
    const placeHolder = ref("maicol")
    const favoriteAnimal = ref<Animal>()
    const animals = ref([
  { id: "1", name: "León" },
  { id: "2", name: "Tigre" },
  { id: "3", name: "Elefante" },
  { id: "4", name: "Jirafa" },
  { id: "5", name: "Cebra" },
  { id: "6", name: "Gorila" },
  { id: "7", name: "Panda" },
  { id: "8", name: "Águila" },
  { id: "9", name: "Lobo" },
  { id: "10", name: "Serpiente" }
]);



   
    const isVisiblecompetitionRegistration = ref(false);
    const isVisibleRegisterplayer = ref(false);
    const isVisiblestartCompetition = ref(false);
    const startCareer = ref(false);
    function register(competion: CompetitionT) {
      currentCompetition.value = competion
      listCompetition.value.push(currentCompetition.value)
      isVisiblecompetitionRegistration.value = false
      isVisiblestartCompetition.value = true
      fetchCompetitions();
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
      isVisibleRegisterplayer.value = true; //fix after 
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



    async function podiumFinal(podium: Results[]) {
      await fecthPodiums()
    }

    function animalUpdate(animal: Animal){
      favoriteAnimal.value = animal
      
    }

    async function fetchCompetitions(){
            const getCompetitions = new CompetitionClientFetch()
            const allCompetitions = await getCompetitions.getCompetitions()
            for (const comp of allCompetitions){
                comps.value.push({id: comp.id , name:comp.name, lapsCount: comp.laps, players: comp.players })
            }
        }

     async function fecthPodiums() {
      const getPodium = new CompetitionClientFetch()
            const allPodiums = await getPodium.getPodiums()
            console.log("the all podiums:", allPodiums)
            for (const pod of allPodiums){
                if(pod.place1 != 0 || pod.place2 != 0 || pod.place3 != 0){
                  podiumPlayers.value.push({id: pod.id_player , name:pod.name, place1:pod.place1, place2:pod.place2, place3: pod.place3})
                }
                
            }
      
      
     }

        onMounted(async () => {
                await fetchCompetitions();
                await fecthPodiums();
        });


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
      showStartcompetition,
      comps,
      nameSelect,
      placeHolder,
      animals,
      animalUpdate,
      favoriteAnimal
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

    <Select2Component v-bind:data="animals" v-bind:name="nameSelect" v-bind:placeholder="placeHolder" v-on:update:value="animalUpdate"> </Select2Component>
    <p>the favorite animal is</p>
    <p>{{ favoriteAnimal?.name }}</p>

    <PlayerRegistration v-on:registered="registerPlayer" v-if="isVisibleRegisterplayer"> </PlayerRegistration>


    
    <CompetitionRegistration v-if="isVisiblecompetitionRegistration " v-on:register="register" v-bind:players="playersRegistered"  >
    </CompetitionRegistration>


  

    <div v-for="comp in comps">
      <Competition v-if="isVisiblestartCompetition" v-bind:competitionProp="comp" v-on:podiumFinal="podiumFinal"></Competition>
    </div>

    
    
   
  </main>

  <div class="global-podium">
      <p>Global podium</p>
      <div v-for="pplayer in podiumPlayers">
    {{ pplayer.name }} 
    <p>first place={{ pplayer.place1 }}</p>
    <p>second place={{ pplayer.place2 }}</p>
    <p>third place={{ pplayer.place3 }}</p>




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
