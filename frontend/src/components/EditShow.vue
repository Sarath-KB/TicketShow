<template>
<div class="background-image-container6">
    <div class="maines" >
    <form  class="form-group" @submit.prevent="updatevenu">
    
    <h1 style="color: white;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EDIT SHOW</h1>

    <div class="childes1" width="100%" style="color: white;font-size: large;">
        <div class="childes2">Show Name:&nbsp;&nbsp;</div>
        <div class="childes3"><input type="text" name="nametxt" placeholder="Enter Show Name" required v-model="name" ><input type="hidden" name="editid" required class="form-control" v-model="editid"></div>
    </div>

    <br/>  

    <div class="childes1" width="100%" style="color: white;font-size: large;">
        <div class="childes2">Rating:</div> 
        <div class="childes3"><input type="number" name="ratenum" placeholder="Enter Rating" required v-model="rating"></div>
    </div>

    <br/> 
        <div class="childes1" width="100%" style="color: white;font-size: large;">
        <div class="childes2">Tag:</div> 
        <div class="childes3"><input type="text" name="ratenum" placeholder="Enter Tag" required v-model="tag"></div>
    </div>

    <br/>

    <div class="childes1" width="100%" style="color: white;font-size: large;"> 
        <div class="childes2">Timing:</div>
        <div class="childes3"><input type="text" name="timetxt"  placeholder="Enter Time" required v-model="timing"></div>
    </div>

     <br/> 

    <div class="childes1" width="100%" style="color: white;font-size: large;"> 
        <div class="childes2">Price:</div>
        <div class="childes3"><input type="number" name="pricenum" placeholder="Enter Price per ticket" required  v-model="price"><input type="hidden" name="editid" required class="form-control" v-model="venue_id"></div>
    </div>
    
    <br/>

    <div class="childes1" width="100%">
        <button type="submit" style="margin: auto;background-color: #555555;font-size: 24px;color: white;">Save</button>
    </div>
    </form>
    </div>
</div>
</template>

<script>
export default {
name:'EditShow',
props:{
    id:{
        type:[Number,String],
        required:true
    }
},
data(){
    return {
         name:null,
         rating:null,
         tag:null,
         timing:null,
         price:null,
         editid:null,
         venue_id:null,
         token:null
             
    }
},
methods:{
    getshow()
{
fetch(`http://127.0.0.1:5000/getdshow/${this.editid}`,{
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
    this.rating=data.data[0].rating
    this.tag=data.data[0].tag
    this.timing=data.data[0].timing
    this.price=data.data[0].price
    this.venue_id=data.data[0].venue_id
})
  
},
updatevenu()
{
    if (!this.name || !this.rating || !this.tag || !this.timing|| !this.price)
    {
        this.error="Error"
        console.log(this.error)
    }
    else{
        fetch(`http://127.0.0.1:5000/updateshow`,{
            method:"POST",
            headers:{
                "content-type":"application/json",
                "x-access-token":this.token
            },
            body:JSON.stringify({name:this.name,rating:this.rating,tag:this.tag,timing:this.timing,price:this.price,id:this.editid,venid:this.venue_id})
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
{
this.token = localStorage.getItem('token')
this.editid=this.$route.params.id
this.getshow()
}  
}








  






</script>

<style>

    .background-image-container6 {
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('./../assets/show.jpg'); 
        background-size:400px 400px;
        background-position: center ;
        height: 150vh;
    }   
        .maines {
            display: flex;
            width: 500px;
            height: 300px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin-top: -100px;
            margin-left: 10px;




        }

        .childes1 {
            display: flex;
            justify-content: space-between;



        }
        .childes2{
            display: flex;
            
        }
        .childes3{
            display: flex;
            
        }
</style>