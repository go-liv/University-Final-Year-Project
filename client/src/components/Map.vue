<template>
  <section>
    <div id='map_wrap'>
      <a href='https://www.maptiler.com' id='watermark'><img
          src='https://api.maptiler.com/resources/logo.svg' alt='MapTiler logo'/></a>
      <div id='map'></div>
      <pre id='mouse_coor'></pre>
    </div>

    <div id='location_search'>
      <input v-on:keyup.enter='searchLoc' id='search' type='text'
        placeholder='City, street or keywords'>
      <ul>
        <li v-for='place in places' :key='place.id' v-on:click='geocode(place.id)'>
          <a>{{ place.name }}</a>
        </li>
      </ul>
    </div>

    <div id='report'>
      <button @click='reportForm = true'>Report a crime</button>
      <form v-if='reportForm == true'>
        <label for='crimeCategory'>Insert the crime category.</label>
        <input id='crimeCategory' v-model='crimeCategory' type='select' />
        <input id='lat' v-model='lat' type='number' step='0.00000001'/>

        <button type='submit' @click='reportForm = false'>Submit crime!</button>
      </form>
    </div>

    <div id='police_data'>
      <button type='button' v-on:click='resetZoom'>Reset Crimes</button>
      <br />
      <button type='button' v-on:click='searchHere'>Search Here</button>
    </div>

    <div id='error'>
      <a>{{ errorMsg }}</a>
    </div>
  </section>
</template>

<script>
import {
  Map, NavigationControl, Marker, Popup, GeolocateControl,
} from 'maplibre-gl';

import axios from 'axios';

export default {
  name: 'Map',
  data() {
    return {
      // for report form
      reportForm: false,
      crimeCategory: null,
      coordinates: [],

      // for map and crime markers
      apiKey: process.env.VUE_APP_MAPTILER_API_KEY,
      center: [-1.515536654205448, 54.27513856219127],
      zoom: 7,
      fly: null,
      map: null,
      places: [{}],
      crimeData: null,
      errorMsg: null,
      addedPopups: null,
    };
  },
  methods: {
    resetZoom() {
      this.fly = 7;
      this.map.flyTo({
        center: this.map.center,
        zoom: this.fly,
        essential: true,
      });
      console.log('removing markers');
      this.addedPopups.forEach((marker) => {
        marker.remove();
      });
      this.addedPopups = null;
      this.crimeData = null;
      this.errorMsg = null;
    },
    searchHere() {
      if (this.map.getZoom() < 11) {
        this.errorMsg = 'The search is too high, lower your zoom to get the results.';
        return;
      }
      this.fly = this.map.getZoom();
      this.getPoliceCrimes();
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
          if (id.includes('county')) {
            this.fly = 10;
          }
          if (id.includes('city')) {
            this.fly = 12;
          }
          if (id.includes('street')) {
            this.fly = 16;
          }
          if (id.includes('subcity')) {
            this.fly = 14;
          }
          this.map.flyTo({
            center: this.center,
            zoom: this.fly,
            essential: true,
          });
          this.places = [{}];
          this.getPoliceCrimes();
        })
        // queryRes = response.data.features[0].center;
        .catch((error) => { console.log(error); });
    },
    getPoliceCrimes() {
      let sw = null;
      let se = null;
      let nw = null;
      let ne = null;
      if (this.fly <= 12 || this.fly >= 11) {
        sw = {
          lat: String(this.center[1] - 0.02765),
          lon: String(this.center[0] - 0.13175),
        };
        se = {
          lat: String(this.center[1] + 0.02765),
          lon: String(this.center[0] - 0.13175),
        };
        nw = {
          lat: String(this.center[1] - 0.02765),
          lon: String(this.center[0] + 0.13175),
        };
        ne = {
          lat: String(this.center[1] + 0.02765),
          lon: String(this.center[0] + 0.13175),
        };
      }
      if (this.fly <= 14 || this.fly >= 13) {
        sw = {
          lat: String(this.center[1] - 0.00705),
          lon: String(this.center[0] - 0.03285),
        };
        se = {
          lat: String(this.center[1] + 0.00705),
          lon: String(this.center[0] - 0.03285),
        };
        nw = {
          lat: String(this.center[1] - 0.00705),
          lon: String(this.center[0] + 0.03285),
        };
        ne = {
          lat: String(this.center[1] + 0.00705),
          lon: String(this.center[0] + 0.03285),
        };
      }
      if (this.fly <= 16 || this.fly >= 15) {
        sw = {
          lat: String(this.center[1] - 0.0035),
          lon: String(this.center[0] - 0.0165),
        };
        se = {
          lat: String(this.center[1] + 0.0035),
          lon: String(this.center[0] - 0.0165),
        };
        nw = {
          lat: String(this.center[1] - 0.0035),
          lon: String(this.center[0] + 0.0165),
        };
        ne = {
          lat: String(this.center[1] + 0.0035),
          lon: String(this.center[0] + 0.0165),
        };
      }

      const url = `https://data.police.uk/api/crimes-street/all-crime?poly=${sw.lat},${sw.lon}:${se.lat},${se.lon}:${nw.lat},${nw.lon}:${ne.lat},${ne.lon}`;
      axios
        .get(url)
        .then((response) => {
          this.crimeData = [];
          response.data.forEach((crime) => {
            const location = {
              type: 'Feature',
              properties: {
                type: 'police',
                category: crime.category,
                month: crime.month,
              },
              geometry: {
                type: 'Point',
                coordinates: [Number(crime.location.longitude), Number(crime.location.latitude)],
              },
            };
            this.crimeData.push(location);
          });
          this.getDBCrimes();
        })
        .catch((error) => {
          console.log(error);
          if (error.status === 503) {
            this.errorMsg = 'Too many crimes reported in the current screen, zoom in!';
            this.crimeData = null;
          }
          if (error.status === 500) {
            this.errorMsg = 'Try again, the API had some trouble reaching our server!';
            this.crimeData = null;
          }
        });
    },
    getDBCrimes() {
      const url = 'http://127.0.0.1:5000/report';
      axios
        .get(url)
        .then((response) => {
          response.data.body.forEach((crime) => {
            this.crimeData.push(crime);
          });
          this.$forceUpdate();
        })
        .catch((error) => {
          if (error.status === 500) {
            this.errorMsg = 'Try again, the API had some trouble reaching our server!';
            this.crimeData = null;
          }
        });
    },
  },
  mounted() {
    console.log(`Geolocation: ${navigator.geolocation}`);
    const geolocate = new GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true,
      },
      trackUserLocation: true,
    });
    this.map = new Map({
      container: 'map',
      style: `https://api.maptiler.com/maps/streets/style.json?key=${this.apiKey}`,
      center: this.center,
      zoom: this.zoom,
    }).addControl(new NavigationControl(), 'top-left')
      .addControl(geolocate, 'top-left');

    console.log(`This center: ${this.center}`);

    this.map.scrollZoom.enable();

    geolocate.on('geolocate', () => {
      this.fly = 16;
    });

    this.map.on('mousemove', (cursor) => {
      document.getElementById('mouse_coor').innerHTML = `${JSON.stringify(cursor.lngLat.wrap())}`;
    });

    this.map.on('zoomend', () => {
      this.fly = this.map.getZoom();
      if (this.fly >= 15 && this.crimeData === null) {
        console.log(`on zoomend, zoom to go to: ${this.fly}`);
        this.getPoliceCrimes();
      }
      if (this.map.getZoom() <= 7
      && !(this.addedPopups === null
      || this.addedPopups === undefined
      || this.addedPopups === [])) {
        this.resetZoom();
      }
    });
  },
  updated() {
    if (this.crimeData !== null && this.addedPopups === null) {
      console.log('adding markers');
      // const el = document.createElement('div');
      // el.className = 'marker';
      // el.style.backgroundImage = 'https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-plane-512.png';
      // el.style.width = `${this.crimeData[0].properties.iconSize}px`;
      // el.style.height = `${this.crimeData[0].properties.iconSize}px`;

      // el.addEventListener('click', () => {
      //   console.log(`Marker: ${this.crimeData[0].properties.category}`);
      // });

      // add popup markers to map
      this.addedPopups = [];
      const locations = [];
      console.log(`CRIME DATA BEFORE ADDING TO MARKERS: ${this.crimeData}`);
      this.crimeData.forEach((crime) => {
        try {
          let exists = 0;
          const [lon, lat] = crime.geometry.coordinates;
          if (this.crimeData.length > 300) {
            this.errorMsg = 'Too many crimes reported in the current screen, reset crimes and search for a more detailed location!';
            throw new Error();
          }

          locations.forEach((loc, i) => {
            if (loc.coordinates[0] === lon && loc.coordinates[1] === lat) {
              locations[i].categories.push(crime.properties.category);
              exists += 1;
            }
          });
          if (exists === 0) {
            locations.push({
              coordinates: [lon, lat],
              type: crime.properties.type,
              month: crime.properties.month,
              categories: [crime.properties.category],
            });
          }
          console.log(this.addedPopups);
        } catch (error) {
          console.log(this.errorMsg);
        }
      });
      locations.forEach((popup) => {
        const add = new Marker({ color: '#0000FF' })
          .setLngLat([popup.coordinates[0], popup.coordinates[1]])
          .setPopup(new Popup().setHTML(`<div id='popup'><h2>Category:  </h2><p>${popup.categories}</p>
            </br><h2>Type of data:  </h2><p>${popup.type}</p>
            </br><h2>Month:  </h2><p>${popup.month}</p></div>`).setMaxWidth('300px'))
          .addTo(this.map);
        this.addedPopups.push(add);
      });
    }
  },
  unmounted() {
    this.map.value.remove();
  },
};
</script>

<style scoped>
@import '~maplibre-gl/dist/maplibre-gl.css';

@font-face {
    font-family: buttons;
    src: url('../assets/fonts/nunito/Nunito-Black.ttf');
}
@font-face {
    font-family: small;
    src: url('../assets/fonts/nunito/Nunito-Light.ttf');
}

/* This won't function as conventional css so see it as a label so I can copy the colors easily */
.theme {
    --primary: rgb(65, 37, 0);
    --secondary: rgb(122, 93, 55);
    --accent: rgb(27, 23, 19);
    --font-color: rgb(243, 211, 170);
    --buttons: buttons;
    --text: small;
}

#report {
    color: rgb(27, 23, 19);
    font-family: buttons;
    position: absolute;
    width: 10%;
    height: 5%;
    left: 88.5%;
    top: 15%;
    text-size-adjust: auto;
    z-index: 998;
}

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
  left: 32%;
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
  left: 76%;
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
  left: 7%;
  top: 4%;
  z-index: 1000;
}

#popup {
  position: absolute;
  z-index: 1001;
}

#error {
  background-color: red;
  color: white;
  position: absolute;
  left: 0%;
  top: 82%;
  font-size: 18px;
  z-index: 1002;
}

@media only screen and (max-width: 800px) {
  #map_wrap {
    position: relative;
    width: 100%;
    height: 80%; /* calculate height of the screen minus the heading */
  }

  #map {
    position: absolute;
    width: 100%;
    height: 80%;
  }

  #watermark {
    position: absolute;
    left: 75%;
    bottom: -18%;
    z-index: 996;
  }

  #mouse_coor {
    display: none;
  }

  #location_search {
    color: rgb(27, 23, 19);
    position: absolute;
    width: 50%;
    height: auto;
    left: 15%;
    top: 2%;
    resize: none;
    z-index: 998;
  }

  #location_search > input {
    font-size: 22px;
    font-family: small;
  }

  #location_search > ul {
    list-style-type: none;
    background-color: rgb(255, 255, 255, 0.85);
    z-index: 999;
    position: absolute;
    text-align: left;
    left: 0;
    padding-left: 2%;
  }

  #location_search > ul > li {
    padding: 1%;
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
    color: rgb(27, 23, 19);
    position: absolute;
    left: 15%;
    top: 10%;
    font-family: buttons;
    z-index: 997;
    width: 50%;
  }

  #popup {
    position: absolute;
    z-index: 1001;
  }

  #error {
    background-color: red;
    color: white;
    position: absolute;
    left: 0%;
    top: 82%;
    font-size: 18px;
    z-index: 1002;
  }
}
</style>
