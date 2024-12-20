<script lang="ts">

import { defineComponent, ref, toRaw, onMounted } from "vue"
import type { PropType } from "vue";
import type { Competition, Player, Results, CompetitionStarted } from "@/models";
import Cronometer from "./Cronometer.vue";
import {CompetitionClientFetch} from '@/client'





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
        competitionProp: {
            type: Object as PropType<CompetitionStarted>,
            required: true,
        }
    },
    setup(props, ctx) {
        const  competitionStarted = ref(false);
        const results = ref<Player[]>([]);
        const players = ref<Player[]>([]);
        let counter: number = 0 
        function startCompetition(){
            competitionStarted.value = true

        }

        async function handlerFinished(resultt: Player){

        
            results.value.push(resultt)

            console.log(results.value.length)
            if(results.value.length == 3){
                const pushPodium = new CompetitionClientFetch()
            for (const player of results.value){
                counter = counter+1
                const idplayerpodium = await pushPodium.insertPodium(player.id, props.competitionProp.id, counter)
                console.log("id player podium", idplayerpodium)
            }
                
            }

        }
        async function fetchUser(){
            const getUser = new CompetitionClientFetch()
            for (const player of props.competitionProp.players){
                const user = await getUser.getUser(player)
                players.value.push({id:user.id, name:user.name})
            }
           
            
          



        }

        onMounted(() => {
                fetchUser();
        });

        
        return { competitionStarted, startCompetition, handlerFinished, results, players}
    }
})

</script>

<template>

    <div class="main-container">
        <div>
            <p>{{ competitionProp.name }}</p>
        
        <ul v-for="player in players">
            <li>{{ player.name}}</li>
        </ul>
    </div>
    <div>
        Laps: {{ competitionProp.lapsCount}}
    </div>


    <div>
        <button v-on:click="startCompetition()">start competition</button>

        <div v-if="competitionStarted">

            <ul v-for="(player, index) in players ">
                <label>{{ player.name }}


                    <Cronometer v-bind:laps="competitionProp.lapsCount" v-bind:player="player"  v-on:finished="handlerFinished"></Cronometer>
                </label>

                

            </ul>



        </div>
        
        

    </div>
    
    
    
    </div>
    

    

</template>


<style scoped>
.main-container{
    display: flex;
        justify-content: center;
        align-items: center;
      max-width: 400px;
      margin: 20px auto;
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 10px;
      background-color: #f9f9f9;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      gap: 10px;
      flex-direction: column


}  

.main-container button{

    text-decoration: none;
  margin: 50px 10px;
  color: black;
  border: 0;
  background-color:  #f9f9f9;  
  padding: 4px 10px;
  border: 2px solid black;
  border-radius: 5px;


}

.main-container li{

    padding: 8px 10px;
      margin-bottom: 5px;
      background-color: #e9f5ff;
      border-radius: 5px;
      color: #007bff;
      display: flex;
      align-items: center;
}



</style>