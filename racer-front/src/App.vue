<script lang="ts">
import { defineComponent, ref } from "vue"
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'

export default defineComponent({
  name: "App",
  setup() {
    const hello = ref("world")

    return {
      hello
    }
  }
})
</script>

<template>
  <header>
  </header>

  <main>
    <div>Hello {{ hello }}</div>
  </main>
</template>

<style scoped></style>
