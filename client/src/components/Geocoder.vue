<template>
<section>
  <div id="location_search" class="location_search"></div>
  <pre id="result"></pre>
</section>
</template>

<script>
// import { onMounted } from 'vue';
// import { loadScript } from 'vue-plugin-load-script';
// import '@maptiler/geocoder';
// import mapboxgl from 'mapbox-gl';
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';

export default {
  name: 'Map',
  data() {
    return {
      coor: null,
      addr: null,
      apiKey: process.env.VUE_APP_MAPBOX_API_KEY,
    };
  },
  mounted() {
    const geocoder = new MapboxGeocoder({
      accessToken: this.apiKey,
      types: 'country,region,place,postcode,locality,neighborhood',
    });

    geocoder.addTo('#location_search');

    // Get the geocoder results container.
    const results = document.getElementById('location_search');

    // Add geocoder result to container.
    geocoder.on('result', (e) => {
      results.innerText = JSON.stringify(e.result, null, 2);
    });
  },
};
</script>

<style scoped>
.location_search {
    color: rgb(27, 23, 19);
    position: absolute;
    width: 35%;
    height: 3%;
    left: 68%;
    top: 3%;
    resize: none;
}
.results {
    background-color: rgb(27, 23, 19);;
}
</style>
