import CourseDetails from "./components/CourseDetails.vue";
import HelloWorld from "./components/HelloWorld.vue";
import SignUp from "./components/SignUp.vue";
import { createRouter ,  createWebHistory} from 'vue-router'
const routes = [

    {
        name:"HelloWorld",
        component: HelloWorld,
        path: "/"

    },
    {
        name:"SignUp",
        component:SignUp,
        path:"/signup"
    },
    {
        name:"CourseD",
        component:CourseDetails,
        path:"/coused"
    },
    {
        path: '/profile',
        name: 'ProfileS',
        component: () => import('@/components/ProfileS.vue'),
        props: true
      },
      
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router