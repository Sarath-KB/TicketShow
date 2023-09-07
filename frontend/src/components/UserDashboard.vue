<template>
<div class="divst">
      <ul>
        <li style="float:left;font-size: large;"><router-link to="/userhome">UserDashboard</router-link></li>
        <li style="float:right;font-size: large;"><router-link to="/userprofile">Profile</router-link></li>
        <li style="float:right;font-size: large;"><router-link :to="{name:'login'}">LogOut</router-link></li>
    </ul>
    <router-view></router-view>
</div>
</template>

<script>
export default {
    name:'UserDashboard'

}
// .mount("app")
</script>

<style>
    .divst{
        padding-top:40px;

    }
        ul {
            list-style-type: none;
            margin-top:-40px;
            padding: 0;
            overflow: hidden;
            background-color: black;
        }



        li a {
            display: inline-block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }

        li a:hover:not(.active) {
            background-color: #555555;
        }



</style>