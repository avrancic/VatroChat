import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import 'vue-multiselect/dist/vue-multiselect.css'

import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VueMultiselect from 'vue-multiselect'
import 'mosha-vue-toastify/dist/style.css'

const app = createApp(App)

import VueProgressBar from "@aacassandra/vue3-progressbar"

const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.component('multi-select', VueMultiselect);
app.use(VueProgressBar, {
    color: "#2a9ed4",
    failedColor: "#d42a2a",
    thickness: "5px",
    transition: {
      speed: "0.2s",
      opacity: "0.6s",
      termination: 300,
    },
    autoRevert: true,
    inverse: false,
  })  
app.use(router)

app.mount('#app')