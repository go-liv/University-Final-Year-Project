<template>
<section>
  <div id="map_wrap">
    <a href="https://www.maptiler.com" id="watermark"><img
        src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler logo"/></a>
    <div id="map" ref="map"></div>
    <pre id="mouse_coor"></pre>
  </div>

  <div id="location_search">
    <input v-on:keyup.enter="searchLoc" id="search" type="text"
      placeholder="City, street or keywords">
    <ul>
      <li v-for="place in places" :key="place.id" v-on:click="geocode(place.id)">
        <a>{{ place.name }}</a>
      </li>
    </ul>
  </div>

  <div id="police_data">
    <button v-on:click="getPoliceCrimes">Police</button>
  </div>

  <div id="error">
    <p>{{ errorMsg }}</p>
  </div>
</section>
</template>

<script>
import {
  Map, NavigationControl,
} from 'maplibre-gl';

import axios from 'axios';

export default {
  name: 'Map',
  data() {
    return {
      apiKey: process.env.VUE_APP_MAPTILER_API_KEY,
      map: null,
      places: [{}],
      policeData: null,
      center: [-1.515536654205448, 52.41199188801869],
      zoom: 9,
      errorMsg: null,
    };
  },
  methods: {
    searchLoc() {
      const query = String(document.getElementById('search').value).replace(' ', '_');
      const url = `https://api.maptiler.com/geocoding/${query}.json?key=${this.apiKey}&bbox=-16.105957,49.624946,4.724121,59.411548`;
      axios
        .get(url)
        .then((response) => {
          const res = [];

          for (const each in response.data.features) { // eslint-disable-line
            res.push({
              name: response.data.features[each].place_name,
              id: response.data.features[each].id,
            });
          }

          this.places = res;
        })
        // queryRes = response.data.features[0].center;
        .catch((error) => { console.log(error); });
    },
    geocode(id) {
      const url = `https://api.maptiler.com/geocoding/${id}.json?key=${this.apiKey}`;
      axios
        .get(url)
        .then((response) => {
          this.center = response.data.features[0].center;
          console.log(`Id on geocode ${id}`);
          if (id.includes('city')) {
            this.zoom = 11;
          }
          if (id.includes('street')) {
            this.zoom = 18;
          }
          if (id.includes('subcity')) {
            this.zoom = 15;
          }
          this.map.flyTo({
            center: this.center,
            zoom: this.zoom,
            essential: true,
          });
          this.places = [{}];
          this.policeData = null;
        })
        // queryRes = response.data.features[0].center;
        .catch((error) => { console.log(error); });
    },
    getPoliceCrimes() {
      this.policeData = [];
      const bounds = this.map.getBounds();
      const sw = bounds.getSouthWest();
      const se = bounds.getSouthEast();
      const nw = bounds.getNorthWest();
      const ne = bounds.getNorthEast();
      const url = `https://data.police.uk/api/crimes-street/all-crime?poly=${sw.lat},${sw.lng}:${se.lat},${se.lng}:${nw.lat},${nw.lng}:${ne.lat},${ne.lng}`;
      axios
        .get(url)
        .then((response) => {
          response.data.forEach((crime) => {
            this.policeData.push(crime);
          });
          console.log(this.policeData);
        })
        .catch((error) => {
          console.log(error);
          if (error.response.status === 503) {
            this.errorMsg = 'Too many crimes reported in the current screen, zoom in!';
            this.policeData = null;
          }
        });
    },
  },
  mounted() {
    this.map = new Map({
      container: 'map',
      style: `https://api.maptiler.com/maps/streets/style.json?key=${this.apiKey}`,
      center: this.center,
      zoom: this.zoom,
    }).addControl(new NavigationControl(), 'top-left');

    this.map.on('mousemove', (cursor) => {
      document.getElementById('mouse_coor').innerHTML = `${JSON.stringify(cursor.lngLat.wrap())}`;
    });

    this.map.on('zoom', () => {
      if (this.map.getZoom() >= 11 && this.policeData === null) {
        this.getPoliceCrimes();
      }
      if (this.map.getZoom() < 8 && this.policeData !== null) {
        this.policeData = null;
      }
    });
  },
  updated() {
    console.log('Setup updated.');
  },
  unmounted() {
    this.map.value.remove();
  },
};
</script>

<style scoped>
@import '~maplibre-gl/dist/maplibre-gl.css';

#map_wrap {
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
  z-index: 996;
}

#mouse_coor {
  display: block;
  position: absolute;
  width: 35%;
  left: 15%;
  border: none;
  font-size: 12px;
  text-align: center;
  color: #222;
  background: #fff;
  z-index: 997;
}

#location_search {
  color: rgb(27, 23, 19);
  position: absolute;
  width: 35%;
  height: auto;
  left: 68%;
  top: 3%;
  resize: none;
  z-index: 998;
}

#location_search > ul {
  list-style-type: none;
  background-color: rgba(255, 255, 255, 0.35);
}

#results {
  color: rgb(27, 23, 19);
  background-color: rgb(197, 197, 197);
  position: absolute;
  width: 35%;
  height: auto;
  left: 60%;
  top: 10%;
  resize: none;
  z-index: 999;
}

#police_data {
  position: absolute;
  left: 50%;
  top: 10%;
  z-index: 1000;
}

#error {
  background-color: red;
  color: white;
  position: absolute;
  left: 15%;
  font-size: 12px;
  z-index: 1001;
}
</style>
