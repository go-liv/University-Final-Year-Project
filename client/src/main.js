import { createApp } from 'vue';
import { loadScript } from 'vue-plugin-load-script';
import App from './App.vue';

const app = createApp(App);
app.use(loadScript);
app.mount('#app');
