import 'vue-good-table-next/dist/vue-good-table-next.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'vue-multiselect/dist/vue-multiselect.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import VueGoodTablePlugin from 'vue-good-table-next';
import Multiselect from 'vue-multiselect'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('multiselect', Multiselect)
app.component('VueDatePicker', VueDatePicker)
app.use(VueGoodTablePlugin)

app.mount('#app')
