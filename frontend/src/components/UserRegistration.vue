<template>
<div class="background-image-container1">

    <div class="mainur">
        <div  class="alert-box" v-if="error">
            {{error}}
        </div>
        <br/>
        <form action="/reg" method="post" @submit.prevent="InsertUser">

            <div class="childur1" width="100%" style="color:black;font-size: large;">
                <div class="childur2">Name:</div>
                <div class="childur3"><input type="text" name="nametxt" placeholder="Enter Name" required v-model="name"></div>
            </div>

            <br/>

            <div class="childur1" width="100%" style="color:black;font-size: large;">
                <div class="childur2">Password:</div> 
                <div class="childur3"><input type="password" name="pswrdtxt" placeholder="Enter Password" required v-model="password"></div>
            </div>

            <br/>     

            <div class="childur1" width="100%" style="color:black;font-size: large;"> 
                <div class="childur2">Confirm Password:&nbsp;&nbsp;</div>
                <div class="childur3"><input type="password" name="pswredtxt" placeholder="Enter Password again " required v-model="cnfrmpassword" ></div>
            </div>

            <br/>

            <div class="childur1" width="100%" style="color:black;font-size: large;">
                <div class="childur2">Email:</div>
                <div class="childur3"><input type="email" name="emltxt" placeholder="Enter email " required v-model="email"></div>
            </div>

            <br/>

            <div class="childur1">
                <button type="submit" style="margin: auto;background-color:#2e8b57;font-size: 24px;color: white;">Sign In</button>
                <button type="reset" style="margin: auto;background-color:#b22222;font-size: 24px; color: white;">Cancel</button>
            </div>
        </form>
    </div>

</div>

  
</template>

<script>
export default {
    name:'UserRegistration'
    ,
    data(){
    return{
        name:null,
        password:null,
        cnfrmpassword:null,
        email:null,
        error:null
    }    
    },
methods:{
    InsertUser(){
        if(!this.name || !this.password || !this.cnfrmpassword || !this.email )
        {
            this.error="Please Fill All fileds"
            console.log(this.error)
        }
        else
        {   
            if(this.password == this.cnfrmpassword ){

                fetch('http://127.0.0.1:5000/userreg',{
                    method:"POST",
                    headers:
                    {
                        "content-type":"application/json"  
                    },
                    body: JSON.stringify({name:this.name,password:this.password,email:this.email})
                })

                .then(res=>res.json())
                .then(()=>{
                    this.$router.push(
                        {
                            name:"login"
                        })
                })
                .catch(error=>{
                    console.log(error);
                })
            }
            else{
                this.error="Passwords does not match"
                console.log(this.error)
            }

        }
    }
 }

}
</script>

<style>
    .background-image-container1{
        justify-content: center;
        display: flex;
        align-items: center;
        background-image: url('./../assets/rbg.jpg'); 
        background-size: cover;
        background-position: center;
        height: 100vh;
    }
        .mainur {
            display: flex;
            width: 500px;
            height: 300px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin-top: 50px;
            margin-left: 800px;
            /* border: black solid; */



        }

        .childur1 {
            display: flex;
            justify-content: space-between;



        }
        .childur2{
            display: flex;
            font-size: 24px;
            
        }
        .childur3{
            display: flex;
            
        }
  
        .alert-box{
            display: flex;
            flex-direction: column;
            color: red;
            font-size: 20px;
            font-family: Arial, Helvetica, sans-serif;
        }

</style>