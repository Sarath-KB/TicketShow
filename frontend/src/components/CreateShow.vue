<template>
<div class="background-image-container5">
    <div class="maincs">
        <form  method="post" class="form-group" @submit.prevent="InsertShow">

        <h1 style="color: white;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ADD SHOW</h1>

        <div class="childcs1" width="100%" style="color: white;font-size: large;">
            <div class="childcs2">Show Name:&nbsp;&nbsp;</div>
            <div class="childcs3"><input type="text" name="nametxt" placeholder="Enter Show Name" required v-model="name"></div>
        </div>

        <br/>
            
        <div class="childcs1" width="100%" style="color: white;font-size: large;">
            <div class="childcs2">Rating:</div> 
            <div class="childcs3"><input type="number" name="ratenum" placeholder="Enter Rating" required v-model="rating"></div>
        </div>
        <br/>
        <div class="childcs1" width="100%" style="color: white;font-size: large;">
            <div class="childcs2">Tag:</div> 
            <div class="childcs3"><input type="text" name="ratenum" placeholder="Enter Genre" required v-model="tag"></div>
        </div>

        <br/>
            
        <div class="childcs1" width="100%" style="color: white;font-size: large;"> 
            <div class="childcs2">Timing:</div>
            <div class="childcs3"><input type="text" name="timetxt"  placeholder="Enter Time" required="" v-model="timing"></div>
        </div>

        <br/>

             <div class="childcs1" width="100%" style="color: white;font-size: large;"> 
            <div class="childcs2">Price:</div>
            <div class="childcs3"><input type="number" name="pricenum" placeholder="Enter Price per ticket" required v-model="price"><input type="hidden" name="pricenum" placeholder="Enter Price per ticket" required v-model="ids"></div>
        </div>
    
        <br/>
        <div class="childcs1" width="100%">
            <button type="submit" style="margin: auto;background-color: #555555;font-size: 24px;color: white;">Save</button>

        </div>
        </form>
    </div>
</div>   
</template>

<script>
export default {
    name: 'CreateShow', 

 props:{
    id:{
    
        type:[Number,String],
        required:true
    }
 },
  data(){

    return{
        name :null,
        rating:null,
        tag:null,
        timing:null,
        price:null,
        error:null,
        ids:null,
        token:null
    }    
 },
 methods:{
    InsertShow(){
        if(!this.name || !this.rating || !this.tag || !this.timing|| !this.price || !this.ids)
        {
            this.error="Please Fill All fileds"
            console.log(this.error)
        }
        else
        {
            fetch(`http://127.0.0.1:5000/createshow`,{
                method:"POST",
                headers:
                {
                  "content-type":"application/json" ,
                  "x-access-token":this.token
                },
                body: JSON.stringify({name:this.name,rating:this.rating,tag:this.tag,timing:this.timing,price:this.price,venueid:this.ids})
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
 created() {
    this.token = localStorage.getItem('token')
   this.ids=this.$route.params.id
    this.token = localStorage.getItem('token')
  }
 
}


</script>

<style>
    .background-image-container5 {
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('./../assets/show.jpg'); 
        background-size:400px 400px;
        background-position: center ;
        height: 150vh;
    }
    .maincs {
        display: flex;
        width: 500px;
        height: 300px;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin-top: -70px;
        margin-left: 0px;
    
    }

    .childcs1 {
        display: flex;
        justify-content: space-between;

    }
    .childcs2{
        display: flex;
            
    }
    .childcs3{
        display: flex;
            
    }
    input[type=text],[type=number]
    {
        height:20px;
    }
</style>