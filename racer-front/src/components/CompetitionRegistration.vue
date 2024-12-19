<script lang="ts">

import type { Competition } from "@/models";
import { defineComponent, reactive, toRaw , PropType, ref, onMounted} from "vue";
import type { Player } from "@/models";
import {CompetitionClientFetch} from '@/client'


export default defineComponent({
    name: "CompetitionRegistration",
    emits: {
        register(payload: Competition) {
            return typeof payload === "object" &&
                typeof payload.name === "string" &&
                typeof payload.lapsCount === "number" &&
                Array.isArray(payload.players)
        }
    },
    props: {
        players: {
            type: Array as PropType<Player[]>,
            required: true,
        },
        
    },
    setup(props, ctx) {

         console.log("Players received in CompetitionRegistration:", props.players);
        const competition = reactive<Competition>({
            name: "",
            lapsCount: 0,
            players: []
        })
        
        const users = ref<{ id: string; name: string }[]>([]);
        const checkedNames = ref<Player>({ id: "",name: "" });
        const playersT = ref<Player[]>([]);
        const playersO = ref<Player[]>([]);
        const removeChecker = ref<Player>({ id: "", name: "" });
        const idPlayers : string[] = []

        
        
        async function save() {
            for (const player of playersT.value){
                idPlayers.push(player.id)
            }
            
            const clientCreateplayer = new CompetitionClientFetch(); 
            const competitionCreated = await clientCreateplayer.createCompetition(competition.name, competition.lapsCount, idPlayers);

            console.log("created comp:", competitionCreated)

    
            const payload = toRaw(competition)
            ctx.emit("register", payload)
        };
        function addPlayer(){
            playersT.value.push(checkedNames.value)
            playersO.value = playersO.value.filter(item => item !== checkedNames.value);
            checkedNames.value = {id: "", name: ""}
        }

        function removePlayer(){
            playersO.value.push(removeChecker.value)
            playersT.value = playersT.value.filter(item => item !== removeChecker.value);
            removeChecker.value = {id: "", name: ""}


        }

        async function fetchUsers(){
            const getUsers = new CompetitionClientFetch()
            const allusers = await getUsers.getUsers()
            users.value = allusers
            console.log("ojala si tenga", users.value)
            console.log("allusers", allusers)
            for (const player of allusers){
                console.log("jugador",player.name)
                playersO.value.push({id:player.id, name:player.name})
            }
          
            console.log("los valores",playersO.value)


        }

        onMounted(() => {
                fetchUsers();
        });

        

    

        return {
            competition,
            save,
            checkedNames, 
            addPlayer,
            playersT,
            playersO,
            removeChecker,
            removePlayer
        }
    }
})

</script>

<template>
    <form v-on:submit.prevent="save">
        <p>Create a competition</p>

        <div>
            <label>Name:
                <input type="text" v-model="competition.name">
            </label>
        </div>
        <div>

            <label>Laps:
                <input type="number" name="laps" v-model="competition.lapsCount">
            </label>
        </div>
        <div>
            <select v-model="checkedNames">
            <option v-for="player in playersO" v-bind:value="player">
             {{ player.name}}
            </option>
            </select>

        </div>
        
        <button type="button"  v-on:click="addPlayer">addPlayer</button>
        <div>
            <select v-model="removeChecker">
            <option v-for="player in playersT" v-bind:value="player">
             {{ player.name}}
            </option>
            </select>
        </div>
        <button type="button"  v-on:click="removePlayer">Remove Player</button>
        <button type="submit">Save</button>
        
    </form>

    

</template>


<style scoped>

form{
        display: flex;
        justify-content: center;
        align-items: center;
      width: 400px;
      height: auto;
      margin: 20px auto;
      flex-direction: column;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 10px;
      background-color: #f9f9f9;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      gap: 10px;

}
form button{
  text-decoration: none;
  margin: 0 10px;
  color: black;
  border: 0;
  background-color:  #f9f9f9;  
  padding: 10px;
  border: 2px solid black;
  border-radius: 5px;

}

form button:hover {
      background-color: #0056b3;
      color: #ffdd00;
      transform: scale(1.1); 
    }

form select{
    width: 100%;
      padding: 10px;
      border: 2px solid #ccc;
      border-radius: 8px;
      background-color: white;
      font-size: 16px;
      color: #333;
}

</style>