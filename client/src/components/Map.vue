<template>
  <div id="map-wrap">
    <a href="https://www.maptiler.com" id="watermark"><img
        src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler logo"/></a>
    <div id="map" ref="mapContainer"></div>
    <pre id="info"></pre>
    <div id="location_search">
      <input type="text" id="search" placeholder="location search" />
      <p id="results">{{lat}} == {{lon}}</p>
    <button type="submit" v-on:click="mvToLoc" />
  </div>
  </div>
</template>

<script>
import {
  Map, NavigationControl,
} from 'maplibre-gl';

import {
  shallowRef, onMounted, onUnmounted, markRaw,
} from 'vue';

import Geocoder from './Geocoder.vue';

export default {
  name: 'Map',
  data() {
    return {
      lat: null,
      lon: null,
    };
  },
  methods: {
    mvToLoc() {
      const query = document.getElementById('search').value;
      [this.lat, this.lon] = Geocoder.geocode(query);
    },
  },
  setup() {
    const apiKey = process.env.VUE_APP_MAPTILER_API_KEY;
    const mapContainer = shallowRef(null);
    const map = shallowRef(null);

    onMounted(() => {
      const initialState = { lng: -3, lat: 54, zoom: 7 };

      map.value = markRaw(new Map({
        container: mapContainer.value,
        style: `https://api.maptiler.com/maps/streets/style.json?key=${apiKey}`,
        center: [initialState.lng, initialState.lat],
        zoom: initialState.zoom,
      }).addControl(new NavigationControl(), 'top-left'));

      map.value.on('mousemove', (e) => {
        document.getElementById('info').innerHTML = `${JSON.stringify(e.point)}<br />${JSON.stringify(e.lngLat.wrap())}`;
      });
    });

    onUnmounted(() => {
      map.value.remove();
    });

    return {
      map, mapContainer,
    };
  },
};
</script>

<style scoped>
@import '~maplibre-gl/dist/maplibre-gl.css';

#map-wrap {
  position: relative;
  width: 100%;
  height: 100%; /* calculate height of the screen minus the heading */
}

#map {
  position: absolute;
  width: 100%;
  height: 100%;
}

#watermark {
  position: absolute;
  left: 10px;
  bottom: 10px;
  z-index: 998;
}

#info {
  display: block;
  position: absolute;
  width: 50%;
  border: none;
  border-radius: 3px;
  font-size: 12px;
  text-align: center;
  color: #222;
  background: #fff;
}

#location_search {
  color: rgb(27, 23, 19);
  position: absolute;
  width: 35%;
  height: auto;
  left: 68%;
  top: 3%;
  resize: none;
}

#results {
  color: rgb(27, 23, 19);
  background-color: aquamarine;
  position: absolute;
  width: 35%;
  height: auto;
  left: 60%;
  top: 10%;
  resize: none;
  z-index: 999;
}
</style>
