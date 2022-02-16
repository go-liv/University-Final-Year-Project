<template>
  <div class="map-wrap">
    <a href="https://www.maptiler.com" class="watermark"><img
        src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler logo"/></a>
    <div class="map" ref="mapContainer"></div>
  </div>
</template>

<script>
import {
  Map, NavigationControl,
} from 'maplibre-gl';

import {
  shallowRef, onMounted, onUnmounted, markRaw,
} from 'vue';

export default {
  name: 'Map',
  setup() {
    const apiKey = process.env.VUE_APP_MAPTILER_API_KEY;
    const mapContainer = shallowRef(null);
    const map = shallowRef(null);

    onMounted(() => {
      const initialState = { lng: -3, lat: 54, zoom: 5 };

      map.value = markRaw(new Map({
        container: mapContainer.value,
        style: `https://api.maptiler.com/maps/streets/style.json?key=${apiKey}`,
        center: [initialState.lng, initialState.lat],
        zoom: initialState.zoom,
      }).addControl(new NavigationControl(), 'top-left'));
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

.map-wrap {
  position: relative;
  width: 100%;
  height: 100%; /* calculate height of the screen minus the heading */
}

.map {
  position: absolute;
  width: 100%;
  height: 100%;
}

.watermark {
  position: absolute;
  left: 10px;
  bottom: 10px;
  z-index: 998;
}
</style>
