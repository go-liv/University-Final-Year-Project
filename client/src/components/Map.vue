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
    <button v-on:click="resetZoom">Reset Crimes</button>
  </div>

  <div id="error">
    <p>{{ errorMsg }}</p>
  </div>
</section>
</template>

<script>
import {
  Map, NavigationControl, Marker,
} from 'maplibre-gl';

import axios from 'axios';

export default {
  name: 'Map',
  data() {
    return {
      apiKey: process.env.VUE_APP_MAPTILER_API_KEY,
      center: [-1.515536654205448, 52.41199188801869],
      zoom: 7,
      fly: null,
      map: null,
      places: [{}],
      crimeData: null,
      errorMsg: null,
      addedMarkers: null,
    };
  },
  methods: {
    resetZoom() {
      this.map.flyTo({
        center: this.map.center,
        zoom: 7,
        essential: true,
      });
      this.fly = 7;
      console.log('removing markers');
      this.addedMarkers.forEach((marker) => {
        marker.remove();
      });
      this.addedMarkers = null;
      this.crimeData = null;
    },
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
          if (id.includes('city')) {
            this.fly = 10;
          }
          if (id.includes('street')) {
            this.fly = 14;
          }
          if (id.includes('subcity')) {
            this.fly = 12;
          }
          this.map.flyTo({
            center: this.center,
            zoom: this.fly,
            essential: true,
          });
          this.places = [{}];
        })
        // queryRes = response.data.features[0].center;
        .catch((error) => { console.log(error); });
    },
    getPoliceCrimes() {
      const sw = {
        lat: String(this.center[1] - 0.03),
        lon: String(this.center[0] - 0.15),
      };
      const se = {
        lat: String(this.center[1] + 0.1),
        lon: String(this.center[0] - 0.15),
      };
      const nw = {
        lat: String(this.center[1] - 0.1),
        lon: String(this.center[0] + 0.15),
      };
      const ne = {
        lat: String(this.center[1] + 0.1),
        lon: String(this.center[0] + 0.15),
      };
      const url = `https://data.police.uk/api/crimes-street/all-crime?poly=${sw.lat},${sw.lon}:${se.lat},${se.lon}:${nw.lat},${nw.lon}:${ne.lat},${ne.lon}`;
      axios
        .get(url)
        .then((response) => {
          this.crimeData = [];
          response.data.forEach((crime) => {
            const location = {
              type: 'Feature',
              properties: {
                category: crime.category,
                month: crime.month,
                iconSize: 20,
              },
              geometry: {
                type: 'Point',
                coordinates: [Number(crime.location.longitude), Number(crime.location.latitude)],
              },
            };

            this.crimeData.push(location);
          });
          this.$forceUpdate();
        })
        .catch((error) => {
          console.log(error);
          if (error.status === 503) {
            this.errorMsg = 'Too many crimes reported in the current screen, zoom in!';
            this.crimeData = null;
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

    this.map.on('zoomend', () => {
      console.log(`zoom to go to: ${this.fly}`);
      if (this.fly >= 10 && this.crimeData === null) {
        this.getPoliceCrimes();
      }
      if (this.fly <= 7
      && !(this.addedMarkers === null
      || this.addedMarkers === undefined
      || this.addedMarkers === [])) {
        this.resetZoom();
      }
    });
  },
  updated() {
    if (this.crimeData !== null && this.addedMarkers === null) {
      console.log('adding markers');
      // const el = document.createElement('div');
      // el.className = 'marker';
      // el.style.backgroundImage = 'https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-plane-512.png';
      // el.style.width = `${this.crimeData[0].properties.iconSize}px`;
      // el.style.height = `${this.crimeData[0].properties.iconSize}px`;

      // el.addEventListener('click', () => {
      //   console.log(`Marker: ${this.crimeData[0].properties.category}`);
      // });

      // add marker to map
      this.addedMarkers = [];
      this.crimeData.forEach((crime) => {
        const lat = crime.geometry.coordinates[1];
        const lon = crime.geometry.coordinates[0];
        const marker = new Marker({ color: '#0000FF' })
          .setLngLat([lon, lat])
          .addTo(this.map);
        this.addedMarkers.push(marker);
      });
      console.log(this.addedMarkers);
    }
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
