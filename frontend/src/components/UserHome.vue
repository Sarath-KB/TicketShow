<template>
  <div style="display: flex; flex-direction:row; flex-wrap: wrap; margin-left: 100px;">
    <div style="margin-top:10px;margin-left:150px;">
    <input type="search"  placeholder="search by location/place" v-model="search" v-on:change="getByLocation"><input type="search"  placeholder="search by showname" v-model="name" v-on:change="getByName"><input type="search"  placeholder="search by Tag" v-model="tag" v-on:change="getByTag"><input type="search"  placeholder="search by rating" v-model="rating" v-on:change="getByrating"><input type="search"  placeholder="search by time" v-model="time" v-on:change="getByTime">
    </div>
    <div v-for =" venue in venuelist " :key="venue.id" >
    <div class="mainuh" v-if="checkIfIdExists(venue.id)">
        <h2>&nbsp;&nbsp;Venue:{{venue.name}}&nbsp;&nbsp;<br>
        &nbsp;&nbsp;Location:{{venue.location}}&nbsp;&nbsp;</h2>
    <div v-if="checkIfIdExists(venue.id)">    
    
        <div v-for =" show in showlist" :key="show.id">
            
        <div v-if="show.venu===venue.id">

        <div class="childuh1">
            <br/>
            <div align="center" style="font-size: 20px;">Show:{{show.name}}<br/>Time:{{show.timing}}</div>
            <br/>
            <div align="center"><button><router-link :to="{name:'userbooking',params:{id:show.id}}" style="background-color:black;font-size:20px;color:white">Book</router-link></button></div>
            <br/>
        </div>
        
        </div> <!--if -->
        <br><br/>
        </div> <!-- {% endfor %} -->
       </div><!---->
       <h3 v-else>No Shows</h3>   
        <br/>
    </div>
    </div>  <!-- {% endfor %} -->
</div>

</template>

<script>
export default {
    name:'UserHome',
     data()
    {
        return{
            venuelist:[],
            showlist:[],
            venlist:[],
            token:null,
            search:null,
            place:null,
            tag:null,
            rating:null,
            time:null
        }
    },
    methods:{
        getvenue()
        {
        fetch('http://127.0.0.1:5000/getvenue',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token": this.token
            }
        })
        .then(resp=>resp.json())
        .then(data=>{
            
            this.venuelist.push(...data.data)
            console.log(this.venuelist)
        })
        .catch(error=>{
            console.log(error);
        })
        },


        getshow()
        {
        fetch('http://127.0.0.1:5000/getshows',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token": this.token
            }
        })
        .then(resp=>resp.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            this.venlist.push(...data.vd)
            // console.log(this.venlist)
        })
        .catch(error=>{
            console.log(error);
        })

        },
       checkIfIdExists(idToCheck) {
        // console.log(idToCheck)
      // Method to check if the id exists in the JSON array
      return this.venlist.some(item => item.venue === idToCheck);
    },
    
    getByLocation(){
        if (!this.search)
        {
            this.error="No Search Result"
        }
        else{
        this.venuelist=[]
        fetch(`http://127.0.0.1:5000/venulocation/${this.search}`,{
            method:"GET",
            headers:{
                "content-type":"applicatiion/json",
                "x-access-token": this.token
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.venuelist.push(...data.data)
            console.log(this.venuelist)
        })
        .catch(error=>{
            console.log(error)
        })
        }
    },
    getByName(){
        if (!this.name)
        {
            this.error="No Search Result"
        }
        else{
        this.showlist=[]
        this.venlist=[]
        fetch(`http://127.0.0.1:5000/showname/${this.name}`,{
            method:"GET",
            headers:{
                "content-type":"applicatiion/json",
                "x-access-token": this.token
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            this.venlist.push(...data.vd)
            console.log(this.showlist)
        })
        .catch(error=>{
            console.log(error)
        })
        }
    },

    
    getByTag(){
        if (!this.tag)
        {
            this.error="No Search Result"
        }
        else{
        this.showlist=[]
        this.venlist=[]
        fetch(`http://127.0.0.1:5000/showtag/${this.tag}`,{
            method:"GET",
            headers:{
                "content-type":"applicatiion/json",
                "x-access-token": this.token
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            this.venlist.push(...data.vd)
            console.log(this.showlist)
        })
        .catch(error=>{
            console.log(error)
        })
        }
    },
    getByrating(){
        if(!this.rating)
        {
            this.error="No Search Result"
        }
        else{
        this.showlist=[]
        this.venlist=[]
        fetch(`http://127.0.0.1:5000/showrating/${this.rating}`,{
            method:"GET",
            headers:{
                "content-type":"applicatiion/json",
                "x-access-token": this.token
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            this.venlist.push(...data.vd)
            console.log(this.showlist)
        })
        .catch(error=>{
            console.log(error)
        })
        }
    },
    getByTime(){
        if (!this.time)
        {
            this.error="No Search Result"
        }
        else{
        this.showlist=[]
        this.venlist=[]
        fetch(`http://127.0.0.1:5000/showtime/${this.time}`,{
            method:"GET",
            headers:{
                "content-type":"applicatiion/json",
                "x-access-token": this.token
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            this.venlist.push(...data.vd)
            console.log(this.showlist)
        })
        .catch(error=>{
            console.log(error)
        })
        }
    },

   
    },

     created(){
        this.token = localStorage.getItem('token')
        console.log(this.token)
        this.getvenue()
        this.getshow()
        
    }
   
}
</script>

<style>

        
        .mainuh {
            display: flex;
            flex-direction:column;
            border: white solid;
            width: 300px;
            height: 1000px;
            margin-left: 10px;
            margin-top: 50px;
            margin-bottom: 10px;
            border-radius: 5px;
            align-items: center;
            background-color: #ADD8E6;
            border: black solid;
            
        }

        .childuh1 {
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            border: black solid 2px;
            border-radius: 5px;
            background-color:white;
            width: 150px;
            height: 150px;
            border-radius: 5px;
            margin-top: 15px;
        }
</style>