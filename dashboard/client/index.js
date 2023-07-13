import {createApp} from 'vue'
import App from "./App.vue";
import {createRouter, createWebHistory} from 'vue-router'
import store from './store'
import axios from "axios";
import constant from "./constant";

import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

const routes = [
    // {
    //     path: `/${constant.urlsDefine.matchAll}`,
    //     component: Home
    // },
    // {
    //     path: `/${constant.urlsDefine.signIn}`,
    //     component: Login
    // },
    // {
    //     path: `/${constant.urlsDefine.signUp}`,
    //     component: SignUp
    // },
    // {
    //     path: `/${constant.urlsDefine.courseDetail}/:id`,
    //     component: CourseDetail
    // },
    // {
    //     path: `/${constant.urlsDefine.courseLearning}/:id`,
    //     component: MainLearning
    // },
    // {
    //     path: `/${constant.urlsDefine.dashboard}`,
    //     component: Dashboard,
    //     meta: {
    //         requiresAuth: true
    //     },
    //     children: [
    //         {
    //             path: `${constant.urlsDefine.createCourse}`,
    //             component: CreateCourse
    //         },
    //         {
    //             path: `${constant.urlsDefine.editCourse}/:id/:mode`,
    //             component: CreateCourse
    //         },
    //         {
    //             path: `${constant.urlsDefine.manageCourses}`,
    //             component: ManagementCourses,

    //         },
    //         {
    //             path: `${constant.urlsDefine.manageUsers}`,
    //             component: ManagementUsers
    //         }
    //     ]
    // }
]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

// router.beforeEach((to, from, next) => {
//     if (to.matched.some(record => record.meta?.requiresAuth)) {
//         if (!store.state.isAuthenticated) {
//             next({
//                 path: `/${constant.urlsDefine.signIn}`,
//                 query: {redirect: to.fullPath}
//             })
//         } else {
//             next()
//         }
//     } else {
//         next()
//     }
// })

// async function getUserInfo() {
//     try {
//         let response = await axios.get(`${window.location.origin}/api/account/get-user-info`, {withCredentials: true});
//         if (response.status === 200) {
//             if (response.data.email && response.data.profileUrl) {
//                 store.state.isAuthenticated = true
//             }

//         }
//     } catch {

//     }

// }

const app = createApp(App)
app.use(router);
app.use(store);
app.use(Antd);
app.mount('#app');
