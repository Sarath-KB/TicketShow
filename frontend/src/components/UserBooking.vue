<template>
<div class="background-image-booking">

<div class="mainub">

    <div class="subub">
        <div class="subub1">VENUE:&nbsp;&nbsp;{{vname}}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SHOW:&nbsp;&nbsp;{{showname}}&nbsp;&nbsp;&nbsp;&nbsp;</div>
        <div class="subub2">TIME:&nbsp;&nbsp;{{showtiming}}</div>
    </div>
    <br/>
    <div v-if="vcapacity>0">
    <form  method="post" class="form-group" @submit.prevent="InsertBooking">

        <div class="childub1" width="100%" style="color:black;font-size: large;">
            <div class="childub2">Number:&nbsp;&nbsp;</div>
            <div class="childub3"><input type="number" class="inpnum" id="num" placeholder="number of seats" :max="vcapacity" min="0" v-on:change="getTotal()" v-model="number" ></div>
        </div>
        
        <br/>


        <div class="childub1" width="100%" style="color:black;font-size: large;">
            <div class="childub2">Price/ticket:&nbsp;&nbsp;</div> 
            <div class="childub3"><input type="text" name="pricenum" id="pricenum" v-model="price"></div>
        </div>

        <br/>

        <div class="childub1" width="100%" style="color:black;font-size: large;"> 
            <div class="childub2">Total Price:&nbsp;&nbsp;</div>
            <div class="childub3"><input type="text" id="res" readonly=" "></div>
        </div>
        
        <br/>
        
        <div class="childub1" width="100%">
            <button type="submit" style="margin: auto;background-color:#2e8b57;font-size: 24px;color: white;">Confirm Booking</button>

        </div>
    </form>
    </div>
    <h1 v-else>HOUSE FULL!</h1>
</div>
</div>
  
</template>

<script>
export default {
    name:'UserBooking',
    props:{
    id:{
        type:[Number,String],
        required:true
    }
},
data(){


    return {
        name:null,
        timing:null,
        price:null,
        showid:null,
        venue_id:null,
        showtime:null,
        showname:null,
        showtiming:null,
        vname:null,
        vcapacity:null,
        number:null,
        token:null
    }
},
methods:{
    InsertBooking(){
        if(!this.number)
        {
            this.error="Please Fill The Number Of Seats"
            console.log(this.error)
        }
               else
        {
            fetch(`http://127.0.0.1:5000/booking`,{
                method:"POST",
                headers:
                {
                  "content-type":"application/json",
                   "x-access-token": this.token
                },
                body: JSON.stringify({number:this.number,show_id:this.showid})
            })

            .then(res=>res.json())
            .then(()=>{
                this.$router.push(
                    {
                        name:"userhome"   
                    })
            })
            .catch(error=>{
                console.log(error);
            })
        }
    
    },
    getshow()
{
fetch(`http://127.0.0.1:5000/getshow/${this.showid}`,{
    method:"GET",
    headers:{
        "content-type":"application/json",
        "x-access-token": this.token
    }
})
.then(resp=>resp.json())
.then(data=>{
    //console.log(data)
    this.name=data.data[0].name
    this.timing=data.data[0].timing
    this.price=data.data[0].price
    this.venue_id=data.data[0].venue_id
    this.showname=data.data[0].name
    this.showtiming=data.data[0].timing
    this.vname=data.data[0].ven_name
    this.vcapacity=data.data[0].ven_capacity
})
  
},

 getTotal()
    {
        let qty=document.getElementById("num").value;
        let rate=document.getElementById("pricenum").value;
        let tot=qty*rate;
        document.getElementById("res").value=tot;
    }
},
created()
{
this.token = localStorage.getItem('token')
this.showid=this.$route.params.id
this.getshow()

}  
}


</script>

<style>
    .background-image-booking {
        background-image: url('./../assets/book.jpg'); 
        background-repeat: no-repeat;
        background-size: cover;
        margin-top:-380px;
        /* background-attachment: scroll; */
    }  

        .mainub {
        display: flex;
        width: 800px;
        height: 400px;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin-top:400px;
        padding-top:125px;
        margin-left: 250px;
       



    }

    .inpnum{
        width:170px
    }
    

    .childub1 {
        display: flex;
        justify-content: space-between;
      



    }
    .childub2{
        display: flex;
        font-size: 20px;
       
    }
    .childub3{
        display: flex;
        
        
    }
   .subub{
        display: flex;
        width: 500px;
        height:50px;
        align-items: center;
        justify-content: space-evenly;
        background-color: black;
        border: white solid;
        margin-top: 100px;
        /* font-family: 'Courier New', Courier, monospace; */
        font-size:20px;
        /* border: black solid; */
    }
    .subub1{
        display: flex;
        color: white;
       
        
    }
    .subub2{
        display: flex;
        color: white;
    } 
  
</style>