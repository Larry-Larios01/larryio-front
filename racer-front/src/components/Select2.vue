<template>
    <select class="select" v-model="model">
      <option value=""></option>
    </select>

    <p>the model is {{ model }}</p>
  </template>


  
  <script lang="ts">
  import { defineComponent, ref,onMounted, defineModel} from 'vue';
  import $ from 'jquery';
  import 'select2';
import 'select2/dist/css/select2.min.css';





  
  
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
    emits: ['update:value'],
    setup(props, { emit }) {
      const model = defineModel()
      
      function initSelect(){
        console.log('jQuery:', $);
        console.log('select2:', $.fn.select2);
        console.log("the select 2", $.fn.select2);
        $('.select').select2({
          data: props.data,
          placeholder: props.placeholder,
          allowClear: true,
      });
      console.log('Elementos encontrados:', $('.select').length);

      }

      
        
     
     
      onMounted(() => {
                initSelect();
                $('.select').on("change", function (e) { console.log("hola", $('.select').val());
              

              });
                
        });
      return {model};
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