<script lang="ts">
import { onMounted, PropType, reactive, toRaw } from 'vue';
import { ref, defineComponent } from 'vue';
import type {Player, Results} from '@/models';

export default defineComponent({
  name: 'PlayerRegistration',

  emits: {
    registered(payload: Player[]) {
        return Array.isArray(payload) &&
        payload.every(player => typeof player.name === "string");
    }
},


  setup(props, ctx) { 
 
        const players = ref<Player[]>([]);
        function addPlayer() {
            players.value.push({ name: ""})
        }

        function save(){
            alert("the players have been registered succesfully")
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
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 10px;
      background-color: #f9f9f9;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

}


</style>