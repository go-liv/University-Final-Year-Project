<template>
  <div id="app">
    <Map />
    <Index />
  </div>
</template>

<script>
import Index from './components/Index.vue';
import Map from './components/Map.vue';

export default {
  name: 'App',
  components: {
    Index,
    Map,
  },
};
</script>

<style>
  html {
      background-color: rgb(122, 93, 55);
  }
</style>
