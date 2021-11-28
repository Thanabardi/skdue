import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CalendarDetail from '../views/CalendarDetail.vue'
import SearchCalendar from '../views/SearchCalendar.vue'
import Form from '../views/create_calendar'
import Register from '../views/Register'
import Setting from '../views/Setting'
import ErrorType from '../views/ErrorType'
import Error401 from '../views/Error401'
import Error403 from '../views/Error403'
import Error404 from '../views/Error404'
import Error5xx from '../views/Error5xx'
import ErrorXXX from '../views/ErrorXXX'
import GoogleCallback from '../views/GoogleCallback'


const routes = [
    // {
    //     path: '/',
    //     name: 'Home',
    //     component: Home
    // },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/search',
        name: 'SearchCalendar',
        component: SearchCalendar
    },
    {
        path: '/:calendar_type/:calendar_slug',
        name: 'CalendarDetail',
        component: CalendarDetail
    },
    {
        path: '/create_calendar',
        name: 'CreateCalendar',
        component: Form
    },
    {
        path: '/',
        name: 'Register',
        component: Register
    },
    {
        path: '/setting',
        name: 'Setting',
        component: Setting,
    },
    {
        path: '/:NotFound(.*)*',
        name: 'ErrorType',
        component: ErrorType,
    },
    {
        path: '/error/401',
        name: 'Error401',
        component: Error401
    },
    {
        path: '/error/403',
        name: 'Error403',
        component: Error403
    },
    {
        path: '/error/404',
        name: 'Error404',
        component: Error404
    },
    {
        path: '/error/5xx',
        name: 'Error5xx',
        component: Error5xx
    },
    {
        path: '/error/XXX',
        name: 'ErrorXXX',
        component: ErrorXXX
    },
    {
        path: '/google/callback',
        name: 'GoogleCallback',
        component: GoogleCallback,
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router