<template>
  <main>
    <section id='map' class="map">
      <Map />
      <button class="report">Report a crime</button>
    </section>

    <button id='options' class="options">
      <img src="../assets/filter.png" width='60px'/>
    </button>

    <section id='themes' class='themes'>
      <button id='theme_ancient' class='theme_ancient'>1</button>
      <button id='theme_modern' class='theme_modern'>1</button>
      <button id='theme_hollow' class='theme_hollow'>1</button>
      <p>Themes</p>
    </section>

    <button id='statistics' class='statistics'>
      Statistics
    </button>

    <footer class="footer">
        <p>About</p>
        <p><a href="https://www.flaticon.com/free-icons/filter" title="filter icons">Filter icons created by joalfa - Flaticon</a></p>
        <p><a href="https://www.maptiler.com" title="Maptiller">Maps - Maptiller Cloud</a></p>
        <p><a href="https://maplibre.org/" title="Maplibre">Cursor geolocation - Maplibre</a></p>
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
};
</script>

<style scoped>
@font-face {
    font-family: ancient-buttons;
    src: url("../assets/fonts/nunito/Nunito-Black.ttf");
}
@font-face {
    font-family: ancient-small;
    src: url("../assets/fonts/nunito/Nunito-Light.ttf");
}

/* This won't function as conventional css so see it as a label so I can copy the colors easily */
.theme-ancient {
    --primary: rgb(65, 37, 0);
    --secondary: rgb(122, 93, 55);
    --accent: rgb(27, 23, 19);
    --font-color: rgb(243, 211, 170);
    --buttons: ancient-buttons;
    --text: ancient-small;
}

section {
    color: rgb(27, 23, 19);
    width: 100%;
    height: 100%;
    /* display: grid;
    grid-template-rows: auto auto 1fr auto;
    grid-template-areas: "head"
                        "nav"
                        "main"
                        "foot"; */
}

.map {
    box-shadow: -20px 20px 20px rgb(27, 23, 19);
    color: rgb(27, 23, 19);
    font-family: ancient-small;
    position: absolute;
    /* maxwidth: 80%; */
    width: 80%;
    height: 80%;
    text-align: center;
    background-color: rgb(27, 23, 19);
    top: 30px;
    left: 2%;
}

.map:hover{
    box-shadow: -25px 25px 30px rgb(27, 23, 19);
}

.report {
    color: rgb(27, 23, 19);
    font-family: ancient-buttons;
    position: absolute;
    width: 10%;
    height: 5%;
    left: 88.5%;
    top: 15%;
    text-size-adjust: auto;
}

.statistics {
    color: rgb(27, 23, 19);
    font-family: ancient-buttons;
    position: absolute;
    width: 10%;
    height: 5%;
    left: 2.5%;
    top: 88.5%;
    text-size-adjust: auto;
}

.themes {
    color: rgb(27, 23, 19);
    font-family: ancient-buttons;
    position: absolute;
    width: 10%;
    height: 5%;
    left: 88.5%;
    top: 88.5%;
    text-size-adjust: auto;
}

.options {
    position: absolute;
    background: none;
    border: none;
    left: 93%;
    top: 5%;
    cursor: pointer;
    text-align: center;
}

.options:hover{
    -webkit-transition: transform 0.5s;
    -moz-transition: transform 0.5s;
    -ms-transition: transform 0.5s;
    -o-transition: transform 0.5s;
    transition: transform 0.5s;
    transform: translateX(-20px);
}

a {
    text-decoration: none;
    color: rgb(243, 211, 170);
}

.footer {
    font-family: ancient-buttons;
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
    z-index: 999;
}

.footer > p:first-of-type {
    padding-left: 40px;
}

.footer:hover{
    -webkit-transition: max-height 2s;
    -moz-transition: max-height 2s;
    -ms-transition: max-height 2s;
    -o-transition: max-height 2s;
    transition: max-height 2s;
    max-height: 300px;
}
</style>
