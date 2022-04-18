<template>
  <main>
    <section v-if='firstAccess' id='welcome'>
      <h2>Welcome to WTC (What the crime!?)</h2>
      <p>Here you can find mapped crime extracted from the UK's Police Forces API data.police.uk,
        plus data reported directly from anonymous users (use at your own discretion).</p>
      <p>To search a location for crime, just zoom into the location or search it in the location
        search bar on the top-right corner of the map, you can also press the geolocation
        button on its left side.</p>
      <button v-on:click='firstAccess = false'>Hide instructions</button>
    </section>

    <section id='map'>
      <Map />
    </section>

    <button id='statistics'>
      Statistics
    </button>

    <footer id='footer'>
        <p>About</p>
        <p><a href='https://www.flaticon.com/free-icons/filter' title='filter icons'>Filter icons created by joalfa - Flaticon</a></p>
        <p><a href='https://www.maptiler.com' title='Maptiller'>Maps - Maptiller Cloud</a></p>
        <p><a href='https://maplibre.org/' title='Maplibre'>Mapping library - Maplibre GL</a></p>
    </footer>
  </main>
</template>

<script>
import Map from './Map.vue';

export default {
  name: 'Index',
  components: {
    Map,
  },
  data() {
    return {
      // for first access message
      firstAccess: true,
    };
  },
};
</script>

<style>
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
#theme {
  --primary: rgb(65, 37, 0);
  --secondary: rgb(122, 93, 55);
  --accent: rgb(27, 23, 19);
  --font-color: rgb(243, 211, 170);
  --buttons: buttons;
  --text: small;
}

section {
  color: rgb(27, 23, 19);
  width: 100%;
  height: 100%;
}

#welcome {
  width: 100%;
  height: 100%;
  background-color: rgb(0, 0, 0);
  color: rgb(243, 211, 170);
  position: absolute;
  z-index: 300;
  top: 0;
  left: 0;
  padding-left: 10%;
  padding-top: 5%;
}

#map {
  box-shadow: -20px 20px 20px rgb(27, 23, 19);
  color: rgb(27, 23, 19);
  font-family: small;
  position: absolute;
  /* maxwidth: 80%; */
  width: 85%;
  height: 80%;
  text-align: center;
  background-color: rgb(27, 23, 19);
  top: 30px;
  left: 2%;
}

#map:hover{
  box-shadow: -25px 25px 30px rgb(27, 23, 19);
}

#statistics {
  color: rgb(27, 23, 19);
  font-family: buttons;
  padding: 0.7em 1.7em;
  font-size: 18px;
  border-radius: 0.5em;
  background: rgb(232, 232, 232);
  border: 1px solid hsl(0, 0%, 91%);
  position: absolute;
  width: 10%;
  height: 5%;
  left: 88.5%;
  top: 87%;
  text-size-adjust: auto;
}

a {
  text-decoration: none;
  color: rgb(243, 211, 170);
}

#footer {
  font-family: buttons;
  display: inline-block;
  text-align: left;
  width: 12%;
  color: rgb(197, 197, 197);
  background-color: rgb(27, 23, 19);
  position: absolute;
  bottom: 0;
  left: 0;
  border-radius: 0 50px 0 0;
  padding-left: 15px;
  padding-right: -15px;
  max-height: 45px;
  overflow: hidden;
  z-index: 299;
}

#footer > p:first-of-type {
  padding-left: 30px;
}

#footer:hover{
  -webkit-transition: max-height 2s;
  -moz-transition: max-height 2s;
  -ms-transition: max-height 2s;
  -o-transition: max-height 2s;
  transition: max-height 2s;
  max-height: 300px;
}

@media only screen and (max-width: 1000px) {
  * {
    box-sizing: border-box;
  }

  section {
    color: rgb(27, 23, 19);
    width: 100%;
    height: 100%;
  }

  #welcome {
    width: 100%;
    height: 100%;
    background-color: rgb(0, 0, 0);
    color: rgb(243, 211, 170);
    position: absolute;
    z-index: 300;
    top: 0;
    left: 0;
    padding-left: 10%;
    padding-top: 5%;
  }

  #map {
    color: rgb(27, 23, 19);
    font-family: small;
    position: absolute;
    width: 96%;
    height: 80%;
    text-align: center;
    background-color: rgb(27, 23, 19);
    top: 30px;
    left: 2%;
  }

  #statistics {
    color: rgb(27, 23, 19);
    font-family: buttons;
    padding: 0.7em 1.7em;
    font-size: 18px;
    border-radius: 0.5em;
    background: rgb(232, 232, 232);
    border: 1px solid hsl(0, 0%, 91%);
    position: absolute;
    width: 20%;
    height: 5%;
    left: 2.5%;
    top: 87%;
    text-size-adjust: auto;
  }

  a {
    text-decoration: none;
    color: rgb(243, 211, 170);
  }

  #footer {
    font-family: buttons;
    display: inline-block;
    text-align: left;
    width: 35%;
    color: rgb(197, 197, 197);
    background-color: rgb(27, 23, 19);
    position: absolute;
    bottom: 0;
    left: 0;
    border-radius: 0 50px 0 0;
    padding-left: 15px;
    padding-right: -15px;
    max-height: 45px;
    overflow: hidden;
    z-index: 299;
  }

  #footer > p:first-of-type {
    padding-left: 30px;
  }

  #footer:active{
    max-height: 300px;
  }
}
</style>
