<script lang="ts">
import { onMounted, PropType, reactive } from 'vue';
import { ref, defineComponent } from 'vue';
import type {Player, Results} from '@/models';

export default defineComponent({
  name: 'PlayerRegistration',

  emits: ['registered'],


  setup(props, {emit}) { 
 
        const players = ref<Player[]>([]);
        function addPlayer() {
            players.value.push({ name: "", podium: { place1: 0, place2: 0, place3: 0 }, })
        }

        function save(){
            emit('registered', players)

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
            <div v-for="(player, index) in players" v-bind:key="index">
                <label>Player {{ index + 1 }}
                    <input type="text" v-model="player.name">
                </label>
            </div>
            <button type="button" v-on:click="addPlayer">Add Player</button>
        </div>
        <button type="submit">Save</button>
    </form>

</template>