<script lang="ts">
import { onMounted, PropType, reactive } from 'vue';
import { ref, defineComponent } from 'vue';
import type {Player, Results} from '@/models';

export default defineComponent({
  name: 'Cronometer',

  emits: ['finished'],
  

  props: {
    laps: {
      type: Number, 
      required: true,   
    },
    player: {
      type: Object as PropType<Player>, 
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

    function lap() {
      numbers.value.push(count.value);

      if (!evaluate()){

        result.laps = numbers.value

        emit('finished', result)


      }
    }

    
    const evaluate = () => numbers.value.length < props.laps;

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
    <button v-on:click="pause">pause</button>
    <button v-on:click="stop"> stop </button>
    <button v-if="evaluate()" @click="lap">lap</button>
    <p>{{ count }}</p>

    <li v-for="lap in numbers">
        {{ lap }}
    </li>   

</template>