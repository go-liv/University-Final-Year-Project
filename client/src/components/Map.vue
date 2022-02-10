<template>
  <section class='map_around'>
    <a href="https://www.maptiler.com" class="watermark"><img
    src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler reference"/></a>
    <div class='map' ref="mapContainer"></div>
  </section>
</template>
    <!-- Map -->
    <!-- getData() from /static/js/api_rel.js not working -->
    <!-- <button id="click">
    Click me
    <script>
        let lat= 52.406645267612724;
        let lng= -1.501645719390064;

        $("#click").click(() => {
        getData(lat, lng, returnData);
        });
    </script>
    </button> -->

<script>
/* From https://documentation.maptiler.com/hc/en-us/articles/4413873409809-How-to-display-a-map-in-Vue-js-using-MapLibre-GL-JS */
import Map from 'maplibre-gl';
import {
  shallowRef,
  onMounted,
  onUnmounted,
  markRaw,
} from 'vue';

export default {
  name: 'Map',
  setup() {
    /* creating two reactive objects, shallow to
    avoid deep conversion allowing only the value to be reactive */
    const mapContainer = shallowRef(null);
    const map = shallowRef(null);

    const initialState = { lng: 2.4000, lat: 53.0000, zoom: 3 };
    onMounted(() => {
    /* change this to your own api key
       const apiKey = process.env.MAPTILER_API_KEY; */
      const apiKey = 'e2X4JtWYnn0mEincF42e';

      map.value = markRaw(new Map({
        container: mapContainer.value,
        style: `https://api.maptiler.com/maps/uk-openzoomstack-night/?key=${apiKey}`,
        center: [initialState.lng, initialState.lat],
        zoom: initialState.zoom,
      }));
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

main {
  background-color: rgb(243, 211, 170);
  color: rgb(0, 0, 0);
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  /* display: grid;
  grid-template-rows: auto auto 1fr auto;
  grid-template-areas: "head"
                      "nav"
                      "main"
                      "foot"; */
}
.map_around {
  position: relative;
  width: 100%;
  height: calc(100vh - 77px); /* calculate height of the screen minus the heading */
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
  z-index: 999;
}
</style>
