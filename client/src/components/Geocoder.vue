<script>
// import { onMounted } from 'vue';
// import { loadScript } from 'vue-plugin-load-script';
// import '@maptiler/geocoder';
// import mapboxgl from 'mapbox-gl';
import axios from 'axios';

export default {
  name: 'Geocoder',
  data() {
    return {
      coor: null,
      addr: null,
      lat: null,
      lon: null,
    };
  },
  geocode(query) {
    const apiKey = process.env.VUE_APP_MAPTILER_API_KEY;

    const url = `https://api.maptiler.com/geocoding/${query}.json?key=${apiKey}&bbox=-16.105957,49.624946,4.724121,59.411548`;
    axios
      .get(url)
      .then((response) => { [this.lat, this.lon] = response.data.features[0].center; })
      // queryRes = response.data.features[0].center;
      .catch((error) => { console.log(error); });

    return [this.lat, this.lon];
  },
};
</script>
