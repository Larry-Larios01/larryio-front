<template>
    <select class="selectAnimal">
      <option value=""></option>
      <option v-for="dt in data" v-bind:value="dt.name">
             {{ dt.name}}
            </option>
    </select>
  </template>


  
  <script lang="ts">
  import { defineComponent, ref,onMounted, PropType} from 'vue';
  import $ from 'jquery';
  import type { Animal } from '@/models';





  
  
  export default defineComponent({
    name: 'Select2Component',
    props: {
      data: {
        type: Array as PropType<Animal[]>,
        required: true
      },
      placeholder: {
        type: String,
        default: ''
      },
      name: {
        type: String,
        required: true
      }
    },
    emits: ['update:value'],
    setup(props, { emit }) {
      const element = $('.selectAnimal')
      
      function initSelect(){
        console.log('jQuery:', $);
        console.log('select2:', $.fn.select2);
        console.log("the select 2", $.fn.select2);
        element.select2({
          placeholder: props.placeholder,
          allowClear: true,
      });
      console.log('Elementos encontrados:', $('.selectAnimal').length);
      }

      element.on('change', () => {
        emit('update:value', element.val());
      });
     
      onMounted(() => {
                initSelect();
        });
      return {};
    }
  });
  </script>
  
  <style scoped>
    select{
      width: 100%;
      padding: 10px;
      border: 2px solid #ccc;
      border-radius: 8px;
      background-color: white;
      font-size: 16px;
      color: #333;
      
  }

  </style>