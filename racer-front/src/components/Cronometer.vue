<script lang="ts">
import { onMounted, PropType, reactive } from 'vue';
import { ref, defineComponent } from 'vue';
import type {Player, Results, PodiumPlayerLap} from '@/models';
import {CompetitionClientFetch} from '@/client'

export default defineComponent({
  name: 'Cronometer',

  emits: ['finished'],
  

  props: {
    laps: {
      type: Number, 
      required: true,   
    },
    player: {
      type: Object as PropType<PodiumPlayerLap>, 
      default:  "unknow",
    },
  },


  setup(props, {emit}) { 
    const count = ref(0);
    let cronometer: number;
    const numbers = ref<number[]>([]);
      const result = reactive<Results>({
      player: props.player,
      laps: [], 
    });

    let counter: number = 0;

    function start() {
      cronometer = setInterval(() => {
      count.value++;
      }, 1000);
    }

    function pause() {
      clearInterval(cronometer);
    }

    function stop() {
      count.value = 0;     
       clearInterval(cronometer);
      numbers.value = [];
    }

     async function lap() {
      //numbers.value.push(count.value);
      if(evaluate()){
        counter = counter+1

      const pushPodium = new CompetitionClientFetch()
      const idplayerpodium = await pushPodium.insertPodiumLap(props.player.idPlayer, props.player.idCompetition, counter, count.value)
      console.log("id player podium", idplayerpodium)
      }
      

      if (!evaluate()){

        result.laps = numbers.value

        emit('finished', props.player)


      }
    }

    
    const evaluate = () => counter < props.laps;

    onMounted (() => {start();});

    
    return {
      start,
      count,
      stop,
      pause,
      lap,
      numbers,
      evaluate,
    };
  },
});
</script>

<template>
  <div class="main-container">
    <div class="btns">

      <button v-on:click="pause">pause</button>
    <button v-on:click="stop"> stop </button>
    <button v-if="evaluate()" @click="lap">lap</button>


    </div>
    
    <p>{{ count }}</p>

    <li v-for="lap in numbers">
        {{ lap }}
    </li>   


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

.btns{
  display: flex;
  flex-direction: row;
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