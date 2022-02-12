<template>
    <textarea name='location_search' cols='1' rows='1'
    placeholder="Street or Postcode" class="location_search">
      <input autocomplete="off" id="location_search" type="text" />
    </textarea>
</template>

<script>
import { onMounted } from 'vue';

export default {
  name: 'Map',
  setup() {
    onMounted(() => {
    const geocoder = new MapboxGeocoder({
      accessToken: 'e2X4JtWYnn0mEincF42e',
    });

    geocoder.on('result', this.input('location_search'));
    });

    return {
      map, mapContainer,
    };
  },
};
</script>

<style scoped>

</style>