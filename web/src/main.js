import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/tailwind.css';

import './scss/variables.scss';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { createVuetify } from 'vuetify';
import { aliases, mdi } from 'vuetify/iconsets/mdi';
import VueVirtualScroller from 'vue3-virtual-scroller'

import '@mdi/font/css/materialdesignicons.css';
import 'vue3-virtual-scroller/dist/vue3-virtual-scroller.css'




const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi', // 使用 mdi 图标集
        aliases,
        sets: {
            mdi,
        },
    },

});

createApp(App)
    .use(router)
    .use(vuetify)
    .use(VueVirtualScroller)
    .mount('#app');
