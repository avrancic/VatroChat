import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"
import 'vue-good-table-next/dist/vue-good-table-next.css'
import 'vue-multiselect/dist/vue-multiselect.css'
import MasonryWall from '@yeger/vue-masonry-wall'

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VueGoodTablePlugin from 'vue-good-table-next';
import VueMultiselect from 'vue-multiselect'

const app = createApp(App)

const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.component('multi-select', VueMultiselect);

app.use(VueGoodTablePlugin)
app.use(router)
app.use(MasonryWall)

app.mount('#app')
