import { createRouter,createWebHistory } from "vue-router";
import AdminDashBoard from './components/AdminDashBoard.vue'
import AdminHome from './components/AdminHome.vue'
import CreateVenue from './components/CreateVenue.vue'
import EditVenue from './components/EditVenue.vue'
import CreateShow from './components/CreateShow.vue'
import EditShow from './components/EditShow.vue'
import UserRegistration from './components/UserRegistration.vue'
import GuestHome from './components/GuestHome.vue'
import Login from './components/Login.vue'
import UserHome from './components/UserHome.vue'
import UserProfile from './components/UserProfile.vue'
import UserBooking from './components/UserBooking.vue'
import GuestDashBoard from './components/GuestDashBoard.vue'
import UserDashBoard from './components/UserDashboard.vue'
import SummaryPage from './components/SummaryPage.vue'
const routes=[
    {
        path:'/admin',
        name:"admin",
        component:AdminDashBoard,
        children:[
            {
                path:'/adminhome',
                name:"adminhome",
                component:AdminHome
            },
            {
                path:'/createvenue',
                name:"createvenue",
                component:CreateVenue
            },
            {
                path:'/editvenue/:id',
                name:"editvenue",
                component:EditVenue,
                params:true
            },
            {
                path:'/createshow/:id',
                name:"createshow",
                component:CreateShow,
                params:true
            },
            {
                path:'/editshow/:id',
                name:"editshow",
                component:EditShow,
                params:true
            },
            {
                path:'/summary/:id',
                name:'summary',
                component:SummaryPage,
                params:true

            }

        ]
    },
   
    {
        path:'/',
        name:'guest',
        component:GuestDashBoard,
        
        children:[
            {
                path:'/',
        name:'guesthome',
        component:GuestHome
            },
            {
                path:'/userreg',
                name:'userreg',
                component:UserRegistration
            },
            {
                path:'/login',
                name:'login',
                component:Login
            },

        ]
    },
    {
        path:'/user',
        name:'user',
        component:UserDashBoard,
        children:[
            {
                path:'/userhome',
                name:'userhome',
                component:UserHome
            },
            {
                path:'/userprofile',
                name:'userprofile',
                component:UserProfile
            },
            {
                path:'/userbooking/:id',
                name:'userbooking',
                component:UserBooking,
                params:true
            }
        ]
    }
   

    
]

const router=createRouter({
    history:createWebHistory(),
    routes
})

export default router;