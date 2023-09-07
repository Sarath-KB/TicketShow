<template>
<div class="divst">
    <ul>
        <li style="float:left;font-size: large;"><router-link to="/adminhome">AdminDashBoard</router-link></li>
        <li style="float:right;font-size: large;"><router-link :to="{name:'login'}">LogOut</router-link></li>
    </ul>
    <router-view></router-view>
</div>
</template>

<script>

export default {
    name:'AdminDashBoard',
   

 
}
</script>

<style>
    .divst{
        padding-top:40px;
        

    }
        

        ul {
            list-style-type: none;
            margin-top: -59px;
            padding: 0;
            width: auto;
            overflow: hidden;
            background-color: black;
        }

        .rl{
            display: inline-block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }

        li a:hover:not(.active) {
            background-color: #555555;
        }

        a {
            text-decoration: none;
        }
</style>