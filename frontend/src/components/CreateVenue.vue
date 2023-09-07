<template >
<div class="background-image-container3">
    <div class="maincv">
        <form @submit.prevent="InsertVenue" method="post" class="form-group">
           
            <h1 style="color: white;">CREATE A VENUE</h1>

            <div class="childcv1" width="100%" style="color: white;font-size: large;">
                <div class="childcv2">Venue Name:&nbsp;&nbsp;</div>
                <div class="childcv3"><input type="text" name="nametxt" placeholder="Enter Venue Name" required v-model="name"></div>
            </div>
            
            <div class="childcv1" width="100%" style="color: white;font-size: large;">
                <div class="childcv2">Place:</div> 
                <div class="childcv3"><input type="text" name="placetxt" placeholder="Enter Place" required v-model="place"></div>
            </div>

            <div class="childcv1" width="100%" style="color: white;font-size: large;"> 
                <div class="childcv2">Location:</div>
                <div class="childcv3"><input type="text" name="locationtxt" placeholder="Enter Location " required v-model="location"></div>
            </div>
            
            <div class="childcv1" width="100%" style="color: white;font-size: large;"> 
                <div class="childcv2">Capacity:</div>
                <div class="childcv3"><input type="number" name="capnum" placeholder="Enter no of seats " required v-model="capacity"></div>
            </div>

            <br/>

            <div class="childcv1" width="100%">
                <button type="submit" style="margin: auto;background-color: #555555;font-size: 24px;color: white;">Save</button>

            </div>

        </form>
    </div>
</div>
</template>

<script>

export default {
 name: 'CreateVenue', 
 data(){
    return{
        name:null,
        place:null,
        location:null,
        capacity:null,
        error:null,
        token:null,
    }    
 },
 methods:{
    InsertVenue(){
        if(!this.name || !this.place || !this.location || !this.capacity)
        {
            this.error="Please Fill All fileds"
            console.log(this.error)
        }
        else
        {
            fetch('http://127.0.0.1:5000/createven',{
                method:"POST",
                headers:
                {
                  "content-type":"application/json" ,
                   "x-access-token": this.token 
                },
                body: JSON.stringify({name:this.name,place:this.place,location:this.location,capacity:this.capacity})
            })

            .then(res=>res.json())
            .then(()=>{
                this.$router.push(
                    {
                        name:"adminhome"
                    })
            })
            .catch(error=>{
                console.log(error);
            })
        }
    }
 },
 created(){
    this.token = localStorage.getItem('token')

 }
}
</script>

<style>
        .maincv {
            display: flex;
            width: 500px;
            height: 350px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin-top: 0px;

        }

        .childcv1 {
            display: flex;
            justify-content: space-between;
            transition: transform 0.3s ease;
            margin-top: 10px;
        }
        .childcv2{
            display: flex;
            transition: transform 0.3s ease;
            margin-top: 10px;    
        }
        .childcv3{
            display: flex;
            transition: transform 0.3s ease;
            margin-top: 10px;
        }

        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color:black;
            border: white solid;
        }


        li a {
            display: inline-block;
            color:white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }

        li a:hover:not(.active) {
            background-color: #555555;
        }

       .background-image-container3 {
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('./../assets/venue.jpg'); 
        background-size: cover;
        background-position: center;
        height: 100vh;
       }
      
       .child1,.child2,.child3:hover{
        transform: scale(1.1);
       }
        
        button{
           padding: auto;
        }

        
        
</style>