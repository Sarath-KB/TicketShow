<template>
<div class="background-image-container4">
     <div class="mainev">
        <form  class="form-group" @submit.prevent="updatevenu">
            <h1 style="color:white;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EDIT VENUE</h1>

            <div class="childev1" width="100%" style="color: white;font-size: large; margin-top: 0px;">
                <div class="childev2">Venue Name:&nbsp;&nbsp;</div>
                <div class="childev3"><input type="text" name="nametxt" placeholder="Enter Venue Name" required class="form-control" v-model="name"> <input type="hidden" name="editid"  required class="form-control" v-model="editid"></div>
            </div>

            <div class="childev1" width="100%" style="color: white;font-size: large;">
                <div class="childev2">Place:</div> 
                <div class="childev3"><input type="text" name="placetxt" placeholder="Enter Place" required class="form-control" v-model="place"></div>
            </div>


            <div class="childev1" width="100%" style="color: white;font-size: large;"> 
                <div class="childev2">Location:</div>
                <div class="childev3"><input type="text" name="locationtxt" placeholder="Enter Location " required class="form-control" v-model="location"></div>
            </div>
            
            <div class="childev1" width="100%" style="color: white;font-size: large;"> 
                <div class="childev2">Capacity:</div>
                <div class="childev3"><input type="number" name="capnum" placeholder="Enter no of seats " required class="form-control"  min="1" v-model="capacity"></div>
            </div>
    
            <div class="childev1" width="100%" style="padding: 25px;">
                <button type="submit" style="margin: auto;background-color: #555555;font-size: 24px;color: white;">Save</button>

            </div>
        
        </form>
    </div>
</div>
</template>

<script>
export default {
name:'EditVenue',
props:{
    id:{
        type:[Number,String],
        required:true
    }
},
data(){
    return {
         name:null,
         place:null,
         location:null,
         capacity:null,
         editid:null,
         error:null ,
         token:null   
    }
},
methods:{
getvenu()
{
fetch(`http://127.0.0.1:5000/getdven/${this.editid}`,{
    method:"GET",
    headers:{
        "content-type":"application/json",
        "x-access-token":this.token
    }
})
.then(resp=>resp.json())
.then(data=>{
    //console.log(data)
    this.name=data.data[0].name
    this.place=data.data[0].place
    this.location=data.data[0].location
    this.capacity=data.data[0].capacity
})
},
updatevenu()
{
    if (!this.name || !this.place || !this.location || !this.capacity)
    {
        this.error="Error"
        console.log(this.error)
    }
    else{
        fetch(`http://127.0.0.1:5000/updatevenu`,{
            method:"POST",
            headers:{
                "content-type":"application/json",
                "x-access-token":this.token
            },
            body:JSON.stringify({name:this.name,place:this.place,location:this.location,capacity:this.capacity,id:this.editid})
        })
        .then(resp=>resp.json())
        .then(()=>{
            this.$router.push({
                name:'adminhome'
            })
        })
    }
}
},
created()
{this.token = localStorage.getItem('token')
this.editid=this.$route.params.id
this.getvenu()
}

}
</script>

<style>
        .mainev {
            display: flex;
            width: 500px;
            height: 350px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin-top:-150px;
          
           

            /* border: 1px solid white; */


        }

        .childev1 {
            display: flex;
            justify-content: space-between;
            transition: transform 0.3s ease;
            margin-top: 10px;


        }
        .childev2{
            display: flex;
            transition: transform 0.3s ease;
            margin-top: 10px;
            
        }
        .childev3{
            display: flex;
            transition: transform 0.3s ease;
            margin-top: 10px;
        }


        
    .background-image-container4 {
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('./../assets/venue.jpg'); 
        background-size: cover;
        background-position: center;
        height: 100vh;
    }
      
    .childev1,.childev2,.childev3:hover{
        transform: scale(1.1);
    }
        
    button{
        padding: auto;
    }
</style>