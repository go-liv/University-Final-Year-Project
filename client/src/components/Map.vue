<template>
  <section>
    <a href='https://www.maptiler.com' id='watermark'><img
          src='https://api.maptiler.com/resources/logo.svg' alt='MapTiler logo'/></a>
    <div id='map'></div>
    <pre id='info'></pre>

    <div id='location_search'>
      <input v-on:keydown.enter='searchLoc(false)' id='search' type='text'
        placeholder='City, street or keywords'>
      <ul>
        <li v-for='place in places' :key='place.name' v-on:click='geocode(place.name, true)'>
          <a>{{ place.name }}</a>
        </li>
      </ul>
    </div>

    <div id='report' v-if='isReport === false'>
      <button v-on:click='isReport = true'>Report a crime</button>
    </div>

    <div id='reportForm' v-if='isReport === true'>
      <form @submit.prevent='reportCrime'>
        <input v-on:keydown.enter.prevent='searchLoc(true)' id='searchInReport' type='text'
        placeholder='City, street or keywords'>
        <ul v-if='placesReport'>
          <li v-for='place in placesReport' :key='place.name'
          v-on:click='geocode(place.name, false)'>
            <a>{{ place.name }}</a>
          </li>
        </ul>
        <label for='month'>Month</label><br/>
        <month-picker-input id='month' @change='changeReportMonth'></month-picker-input>
        <label for='category'>Category</label><br/>
        <select name='category' id='category' v-model='this.crimeCategory'>
          <option value='anti-social-behaviour'>Anti-social behaviour</option>
          <option value='bicycle-theft'>Bicycle theft</option>
          <option value='burglary'>Burglary</option>
          <option value='criminal-damage-arson'>Criminal damage and arson</option>
          <option value='drugs'>Drugs</option>
          <option value='other-theft'>Other theft</option>
          <option value='possession-of-weapons'>Possession of weapons</option>
          <option value='public-order'>Public order</option>
          <option value='robbery'>Robbery</option>
          <option value='shoplifting'>Shoplifting</option>
          <option value='theft-from-the-person'>Theft from the person</option>
          <option value='vehicle-crime'>Vehicle Crime</option>
          <option value='violent-crime'>Violence and sexual offenses</option>
          <option value='other-crime'>Other crime</option>
        </select>
        <button type='button' v-on:click='isReport = false'> Close form </button>
        <button type='submit'> Submit </button>
      </form>
    </div>

    <div id='police_data'>
      <button type='button' v-on:click='resetMarkers'>Reset Crimes</button>
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
import { MonthPickerInput } from 'vue-month-picker';

export default {
  name: 'Map',
  components: {
    MonthPickerInput,
  },
  data() {
    return {
      // for report form
      isReport: false,
      crimeCategory: null,
      coordinates: null,
      date: {
        from: null,
        to: null,
        month: null,
        year: null,
      },
      placesReport: [{}],

      // for map and crime markers
      apiKey: process.env.VUE_APP_MAPTILER_API_KEY,
      travelTime: process.env.VUE_APP_TRAVEL_TIME_API_KEY,
      appId: process.env.VUE_APP_TRAVEL_TIME_APP_ID,
      center: [-0.118092, 51.50986],
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
    changeReportMonth(date) {
      this.date = date;
    },
    reportCrime() {
      console.log('Crime data:');
      console.log(`coordinates: ${this.coordinates}`);
      console.log(`category: ${this.crimeCategory}`);
      console.log(`date: ${JSON.stringify(this.date)}`);
      const url = 'http://127.0.0.1:5000/report';
      axios
        .post(url, {
          coordinates: this.coordinates,
          date: this.date,
          category: this.crimeCategory,
        })
        .then((response) => {
          console.log(`RESPONSE: ${JSON.stringify(response.data.body)}`);
          this.$forceUpdate();
        })
        .catch((error) => {
          if (error.status === 500) {
            this.errorMsg = 'Try again, the API had some trouble reaching our server!';
            this.crimeData = null;
          }
        });
    },
    resetZoom() {
      this.fly = 7;
      this.map.flyTo({
        center: this.map.center,
        zoom: this.fly,
        essential: true,
      });
      this.resetMarkers();
    },
    resetMarkers() {
      console.log('removing markers');
      if (this.addedPopups !== null) {
        this.addedPopups.forEach((marker) => {
          marker.remove();
        });
      }
      this.addedPopups = null;
      this.crimeData = null;
      this.errorMsg = null;
      this.places = null;
      this.placesReport = null;
    },
    searchHere() {
      this.resetMarkers();
      if (this.map.getZoom() < 11) {
        this.errorMsg = 'The search is too high, lower your zoom to get the results.';
        return;
      }
      const centerMv = this.map.getCenter();
      this.center = [centerMv.lng, centerMv.lat];
      this.fly = this.map.getZoom();
      this.getPoliceCrimes();
    },
    searchLoc(report) {
      let query = null;
      if (report) {
        query = String(document.getElementById('searchInReport').value).replace(' ', '_');
      } else {
        query = String(document.getElementById('search').value).replace(' ', '_');
      }
      const url = `https://api.traveltimeapp.com/v4/geocoding/search?query="${query}"&within.country=gb`;
      axios
        .get(url, {
          headers: {
            'X-Api-Key': this.travelTime,
            'X-Application-Id': this.appId,
            'Accept-Language': 'en',
          },
        })
        .then((response) => {
          const res = [];
          for (const each in response.data.features) { // eslint-disable-line
            res.push({
              name: response.data.features[each].properties.name,
            });
          }
          if (report) {
            this.placesReport = res;
          } else {
            this.places = res;
          }
          console.log(`places: ${res}`);
        })
        .catch((error) => { console.error(error); });
    },
    geocode(name, fly) {
      const url = `https://api.traveltimeapp.com/v4/geocoding/search?query="${name}"`;
      this.resetMarkers();
      axios
        .get(url, {
          headers: {
            'X-Api-Key': this.travelTime,
            'X-Application-Id': this.appId,
            'Accept-Language': 'en',
          },
        })
        .then((response) => {
          this.coordinates = response.data.features[0].geometry.coordinates;
          if (fly) {
            this.fly = 16;
            this.map.flyTo({
              center: this.coordinates,
              zoom: this.fly,
              essential: true,
            });
            this.places = [{}];
            this.getPoliceCrimes();
          }
        })
        // queryRes = response.data.features[0].center;
        .catch((error) => { console.error(error); });
    },
    getPoliceCrimes() {
      let sw = null;
      let se = null;
      let nw = null;
      let ne = null;
      if (this.fly <= 12 && this.fly >= 11) {
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
      if (this.fly <= 14 && this.fly >= 13) {
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
      if (this.fly <= 16 && this.fly >= 15) {
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
      console.log('On Police crimes');
      console.log(`This.Fly = ${this.fly}`);
      console.log(`BBOX: ${sw.lat}-${sw.lon} ${se.lat}-${se.lon} ${nw.lat}-${nw.lon} ${ne.lat}-${ne.lon}`);
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
          console.error(error);
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
      console.log('On DB crimes');
      console.log(`ZOOM: ${this.map.getZoom()}`);
      axios
        .get(url, {
          params: {
            lat: this.center[1],
            lon: this.center[0],
            zoom: this.map.getZoom(),
          },
        })
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
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    const geolocate = new GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true,
      },
      trackUserLocation: true,
    });

    this.map = new Map({
      container: 'map',
      style: `https://api.maptiler.com/maps/voyager/style.json?key=${this.apiKey}`,
      center: [this.center[0], this.center[1]],
      zoom: this.zoom,
      maxBounds: [[-7.57216793459, 49.959999905], [1.68153079591, 58.6350001085]],
    }).addControl(new NavigationControl(), 'top-left')
      .addControl(geolocate, 'top-left');

    console.log(`This center on mounted: ${this.map.getCenter()}`);

    this.map.on('mousemove', (e) => {
      document.getElementById('info').innerHTML = `${JSON.stringify(e.point)} <br /> ${JSON.stringify(e.lngLat.wrap())}`;
    });

    this.map.scrollZoom.enable();

    geolocate.on('geolocate', () => {
      this.fly = 16;
    });

    this.map.on('zoomend', () => {
      this.fly = this.map.getZoom();
      if (this.fly >= 15 && this.crimeData === null) {
        console.log(`on zoomend, zoom to go to: ${this.fly}`);
        const centerMv = this.map.getCenter();
        this.center = [centerMv.lng, centerMv.lat];
        this.getPoliceCrimes();
      }
      if (this.map.getZoom() <= 7
      && !(this.addedPopups === null
      || this.addedPopups === undefined
      || this.addedPopups === [])) {
        this.resetMarkers();
      }
    });
  },
  updated() {
    console.log(`This center ${this.center}`);
    if (this.crimeData !== null && this.addedPopups === null) {
      console.log('adding markers');
      // add popup markers to map
      this.addedPopups = [];
      const locations = [];
      console.log(`CRIME DATA BEFORE ADDING TO MARKERS: ${this.crimeData}`);
      this.crimeData.forEach((crime) => {
        try {
          let exists = 0;
          const [lon, lat] = crime.geometry.coordinates;
          if (this.crimeData.length > 400) {
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
          console.error(this.errorMsg);
        }
      });
      locations.forEach((popup) => {
        const add = new Marker({ color: '#0000FF', offset: [0, 0] })
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
    this.map.remove();
  },
};
</script>

<style scoped>
@import '~maplibre-gl/dist/maplibre-gl.css';
@import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css';

@font-face {
    font-family: buttons;
    src: url('../assets/fonts/nunito/Nunito-Black.ttf');
}
@font-face {
    font-family: small;
    src: url('../assets/fonts/nunito/Nunito-Light.ttf');
}

* {
  box-sizing: border-box;
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
  z-index: 200;
}

#reportForm {
    color: rgb(27, 23, 19);
    position: absolute;
    width: 11%;
    height: 40%;
    left: 45.5%;
    top: 3%;
    -webkit-text-size-adjust: auto;
    -moz-text-size-adjust: auto;
    text-size-adjust: auto;
    z-index: 201;
    background: wheat;
}

#map {
  position: relative;
  width: 100%;
  top: 0;
  bottom: 0;
}

#watermark {
  position: absolute;
  left: 10px;
  bottom: 10px;
  z-index: 202;
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
  z-index: 203;
}

#location_search {
  color: rgb(27, 23, 19);
  position: absolute;
  width: 35%;
  height: auto;
  left: 76%;
  top: 3%;
  resize: none;
  z-index: 204;
}

#location_search > ul {
  list-style-type: none;
  left: 10%;
  background-color: rgb(255, 255, 255);
  position: absolute;
  padding-left: 0;
  width: 600px;
  z-index: 205;
}

#location_search > ul > li {
  padding: 1%;
}

#reportForm > form > ul {
  list-style-type: none;
  left: 10%;
  background-color: rgb(255, 255, 255);
  position: absolute;
  padding-left: 0;
  z-index: 205;
}

#reportForm > form > ul > li {
  padding: 1%;
}

#police_data {
  position: absolute;
  left: 7%;
  top: 4%;
  z-index: 206;
}

#error {
  background-color: red;
  color: white;
  position: absolute;
  left: 0%;
  top: 82%;
  font-size: 18px;
  z-index: 207;
}

@media only screen and (max-width: 1000px) {
  * {
    box-sizing: border-box;
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
    z-index: 200;
  }

  #reportForm {
    color: rgb(27, 23, 19);
    position: absolute;
    width: 10%;
    height: 5%;
    left: 88.5%;
    top: 20%;
    text-size-adjust: auto;
    z-index: 201;
  }

  #month {
    right: 50%;
    top: 0;
  }

  #map {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }

  #watermark {
    position: absolute;
    left: 75%;
    bottom: -18%;
    z-index: 202;
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
    z-index: 203;
  }

  #location_search > input {
    font-size: 22px;
    font-family: small;
  }

  #location_search > ul {
    list-style-type: none;
    background-color: rgb(255, 255, 255);
    z-index: 204;
    position: absolute;
    text-align: left;
    left: 0;
    padding-left: 2%;
  }

  #location_search > ul > li {
    padding: 1%;
  }

  #searchInReport {
    list-style-type: none;
    left: 10%;
    background-color: rgb(255, 255, 255);
    position: absolute;
    padding-left: 0;
    z-index: 205;
  }

  #searchInReport > li {
    padding: 1%;
  }

  #police_data {
    color: rgb(27, 23, 19);
    position: absolute;
    left: 15%;
    top: 10%;
    font-family: buttons;
    z-index: 205;
    width: 50%;
  }

  #popup {
    position: absolute;
    z-index: 206;
  }

  #error {
    background-color: red;
    color: white;
    position: absolute;
    left: 0%;
    top: 82%;
    font-size: 18px;
    z-index: 207;
  }
}
</style>
