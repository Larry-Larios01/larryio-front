<script lang="ts">
import { onMounted, PropType, reactive, toRaw } from 'vue';
import { ref, defineComponent } from 'vue';
import type {Player, Results} from '@/models';
import {CompetitionClientFetch} from '@/client'

export default defineComponent({
  name: 'PlayerRegistration',

  emits: {
    registered(payload: Player[]) {
        return Array.isArray(payload) &&
        payload.every(player => typeof player.name === "string" );
    }
},


  setup(props, ctx) { 
 
        const players = ref<Player[]>([]);
        function addPlayer() {
            players.value.push({ id: "", name: ""})
        }

        async function save(){
            const clientCreateplayer = new CompetitionClientFetch(); 
            for (const player of players.value){
                const playerCreated = await clientCreateplayer.createUser(player.name);
                console.log(`Player is created: ${playerCreated.id}`);
            }
          

            const payload = toRaw(players.value)
            ctx.emit("registered", payload)

        }
        return {
            addPlayer,
            players,
            save
            
        }
  },
});
</script>


<template>

    
    <form v-on:submit.prevent="save">
        <div>
            <h3>Add new players</h3>
            <div v-for="(player, index) in players" v-bind:key="index">
                <label>Player {{ index + 1 }}
                    <input type="text" v-model="player.name">
                </label>
            </div>
            <button type="button" v-on:click="addPlayer">Add Player</button>
            <button type="submit">Save</button>
        </div>
       
    </form>

</template>

<style scoped>

form{
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

}
form button{
    text-decoration: none;
  margin: 50px 10px;
  color: black;
  border: 0;
  background-color:  #f9f9f9;  
  padding: 4px 10px;
  border: 2px solid black;
  border-radius: 5px;

}

form button:hover {
      background-color: #0056b3;
      color: #ffdd00;
      transform: scale(1.1); 
    }

form input{
    padding: 10px,10px, 10px, 10px ;
}


</style>