<template>
    <select class="selectAnimal" :name="name">
      <option v-for="dt in data" :key="dt.id" :value="option.id">
        {{ dt }}
      </option>
    </select>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, watch, onMounted, onBeforeUnmount } from 'vue';
  import jQuery from 'jquery';
  import { Select2 } from 'select2';





  
  
  export default defineComponent({
    name: 'Select2Component',
    props: {
      data: {
        type: Array,
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
    emits: ['update:modelValue'],
    setup(props, { emit }) {
      
      
      function initSelect(){
        console.log('jQuery:', $);
        console.log('select2:', $.fn.select2);
        console.log("the select 2", $.fn.select2);
        $('.selectAnimal').select2({
          placeholder: 'Select an option'
      });
      console.log('Elementos encontrados:', $('.selectAnimal').length);
      }
     
      onMounted(() => {
                initSelect();
        });
      return {};
    }
  });
  </script>
  
  <style>
  /* Agrega estilos si es necesario */
  </style>