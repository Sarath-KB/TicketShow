<template>
<div>
    <div style="margin-top:180px; margin-left:615px;"><button><router-link to="/createvenue"><img src="./../assets/add.png"></router-link></button>
        <br/>
        <p style="color:black; font-size: larger;margin-left: -15px;">Add Venue</p>
    </div>

    <div style="display:flex;flex-wrap:wrap;flex-direction:row;">
        
        <div class="mainadm" v-for=" venue in venuelist" :key="venue.id">
            <br/>
            <div class="child" style=" font-size:24px; margin-top: 10px;">Venue:{{venue.name}}</div>
            <br/>

                <div v-if="checkIfIdExists(venue.id)"> 

                <div  v-for="show in showlist" :key="show.id">

                    <div v-if="show.venu===venue.id">

                        <div class="schild">
                            <h3>Show:{{show.name}}<br/>Time:{{show.timing}}</h3>
                            <br/>
                            <div class="child">
                                <button style="margin: auto;background-color:white;font-size: 20px;"><router-link :to="{name:'editshow',params:{id:show.id}}" style="font-size: 20px;color:black; border-radius: 5px;">Edit</router-link></button>&nbsp;&nbsp;
                                <button @click.prevent="delshow(show.id)" style="margin: auto;background-color:white;font-size: 20px; color:black;border-radius: 5px">Delete</button>
                            </div>
                        </div> <!--schild-->
                    </div><!--id if-->
                    <br/>
                </div><!--for-->

                </div><!--empty if-->
                <h2 v-else >NO Shows Available</h2>
                
            <br><br/>
          
            <div class="child">
                <button style="margin: auto;background-color:white;"><router-link :to="{name:'createshow',params:{id:venue.id}}" style="font-size: 20px;color:black; border-radius: 5px;">+</router-link></button>&nbsp;&nbsp;
            </div>
            <br/>

        <br/>
            
            <div class="child">
                <button style="margin: auto;background-color:white"><router-link :to="{name:'editvenue',params:{id:venue.id}}" style="font-size: 20px;color:black; border-radius: 5px;">Edit Venue</router-link></button>&nbsp;&nbsp;
                <button @click.prevent="delvenue(venue.id)" style="margin: auto;background-color:white;font-size: 20px; color:black;border-radius: 5px">Delete Venue</button>
            </div>
            <br/>
            <br/>   
            <div>
            <br/>
                <button class="btn"><router-link :to="{name:'summary',params:{id:venue.id}}" style="color:black;">Download Report</router-link></button>
    
            </div>
        </div>


    
    
</div>    

</div>

   
</template>

<script>
export default {
    name:'AdminHome',
     data()
    {
        return{
            venuelist:[],
            showlist:[],
            venlist:[],
            token:null
        }
    },
    methods:{
        getvenue()
        {
        fetch('http://127.0.0.1:5000/getdvenue',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token":this.token
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
        fetch('http://127.0.0.1:5000/getdshows',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token":this.token
            }
        })
        .then(resp=>resp.json())
        .then(data=>{
            
            this.showlist.push(...data.data)
            console.log(this.showlist)
            this.venlist.push(...data.vd)
        })
        .catch(error=>{
            console.log(error);
        })
        },
        delvenue(id){
            fetch(`http://127.0.0.1:5000/delven/${id}`,{
            method:"DELETE",
            headers:{
                "content-type":"application/json",
                 "x-access-token":this.token
            }
        })
        .then(res=>res.json())
        .then(()=>{
            this.$router.go()
        })

        .catch(error=>{
            console.log(error);
        })

        },
        delshow(id){
            fetch(`http://127.0.0.1:5000/delshow/${id}`,{
            method:"DELETE",
            headers:{
                "content-type":"application/json",
                 "x-access-token":this.token
            }
        })
        .then(res=>res.json())
        .then(()=>{
            this.$router.go()
        })

        .catch(error=>{
            console.log(error);
        })

        },
        checkIfIdExists(idToCheck) {

        // console.log(idToCheck)
      // Method to check if the id exists in the JSON array
        return this.venlist.some(item => item. === idToCheck);
    }venue
        
    },
    created(){
        this.token = localStorage.getItem('token')
        this.getvenue()
        this.getshow()
    }
}
</script>

<style>

        .mainadm {
            display: flex;
            flex-direction:column;
            border: white solid;
            width: 300px;
            height: 1000px;
            margin-left: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            align-items: center;
            background-color: #ADD8E6;
            border: black solid;
            
            
        
        }

        .child {
            display: flex;
            color: black;



        }

        .schild{
            display: flex;
            flex-direction: column;
            border:  black solid;
            background-color: white; 
            width: 175px;
            height: 150px;
            align-items:center;
            border-radius: 5px;
           
           
        }

        .btn {
            background-color: white; 
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            color:black;
            border:black solid;
        }

        ul {
            list-style-type: none;
            margin:0 ;
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

        a {
            text-decoration: none;
        }
</style>