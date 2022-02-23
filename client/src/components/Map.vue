<template>
<section>
  <div id="map-wrap">
    <a href="https://www.maptiler.com" id="watermark"><img
        src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler logo"/></a>
    <div id="map" ref="mapContainer"></div>
    <pre id="info"></pre>
  </div>

  <div id="location_search">
    <input type="text" id="search" placeholder="location search" />
    <button id="submit" type="submit" />
  </div>
</section>
</template>

<script>
import {
  Map, NavigationControl,
} from 'maplibre-gl';

import {
  shallowRef, onMounted, onUnmounted, markRaw,
} from 'vue';

import axios from 'axios';

export default {
  name: 'Map',
  setup() {
    const apiKey = process.env.VUE_APP_MAPTILER_API_KEY;
    const mapContainer = shallowRef(null);
    const map = shallowRef(null);

    onMounted(() => {
      const initialState = { lng: -1.515536654205448, lat: 52.41199188801869, zoom: 12 };

      map.value = markRaw(new Map({
        container: mapContainer.value,
        style: `https://api.maptiler.com/maps/streets/style.json?key=${apiKey}`,
        center: [initialState.lng, initialState.lat],
        zoom: initialState.zoom,
      }).addControl(new NavigationControl(), 'top-left'));

      map.value.on('mousemove', (cursor) => {
        document.getElementById('info').innerHTML = `${JSON.stringify(cursor.point)}<br />${JSON.stringify(cursor.lngLat.wrap())}`;
      });

      document.getElementById('submit').addEventListener('click', () => {
        console.log('submitting query to geocoder');
        console.log('geocoder called');
        const query = document.getElementById('search').value;
        const url = `https://api.maptiler.com/geocoding/${query}.json?key=${apiKey}&bbox=-16.105957,49.624946,4.724121,59.411548`;
        axios
          .get(url)
          .then((response) => {
            console.log(`On geocoder() ${response.data.features[0].center}`);
            map.value.flyTo({
              center: response.data.features[0].center,
              essential: true,
            });
          })
          // queryRes = response.data.features[0].center;
          .catch((error) => { console.log(error); });
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
