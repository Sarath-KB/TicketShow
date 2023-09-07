<template>
<div class="divst">
<ul>
    <li style="float:left;font-size: large;"><router-link to="/userreg">Registration</router-link></li>
    <li style="float:left;font-size: large;"><router-link to="/login">LogIn</router-link></li>
    <li style="float:right;font-size: large;"><router-link to="/login">LogOut</router-link></li>
</ul>
<router-view></router-view>
 </div>
</template>

<script>
export default {
    name:'GuestDashBoard'
    
}
</script>

<style>
    .divst{
        padding-top:40px;

    }
     ul {
            list-style-type: none;
            padding: 0;
            width: auto;
            overflow: hidden;
            background-color: black;
            margin-top: 500px;
        }


        li a:hover:not(.active) {
            background-color: #555555;
        }

        a {
            text-decoration: none;
        }

</style>