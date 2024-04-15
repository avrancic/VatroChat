import 'vue-good-table-next/dist/vue-good-table-next.css'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'vue-multiselect/dist/vue-multiselect.css'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VueGoodTablePlugin from 'vue-good-table-next';
import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(VueGoodTablePlugin)
app.use(router)

app.mount('#app')
