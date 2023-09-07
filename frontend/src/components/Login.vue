<template>
<div class="background-image-container2">
 <div class="mainlg" >
            <h1 style="color:white">{{error}}</h1>
            <form @submit.prevent="login" method="post" class="form-group">

            <div class="childlg1" width="100%" style="color:white;font-size: 24px;">E-mail:<input type="email" name="emltxt" placeholder="Enter Mail ID" v-model="email" ></div>

            <br/>

            <div class="childlg1" width="100%" style="color:white;font-size: 24px;">Password:&nbsp;&nbsp;<input type="password" name="pswrdtxt" placeholder="Enter Password" v-model="password" ></div>
           
            <br>
            <br/>  

            <div class="childlg1" width="100%" >
                <button type="submit"  style="margin: auto;background-color:white;font-size: 24px; color:black">Log In</button>
                <button style="margin:auto;background-color:white;"><router-link style="font-size: 24px; color:black;" to="/userreg">Register</router-link></button>
           </div>
        </form>
    </div>
</div>
 
</template>

<script>
export default {
name:'UserLogin',
data(){
    return {
        email:null,
        password:null,
        error:null
    }
},
    methods:{
        login(){
            if(!this.email || !this.password)
            {
                this.error="Please Fill Fields"
                console.log(this.error)
            }
            else{
                fetch(`http://127.0.0.1:5000/login/${this.email}/${this.password}`,{
                    method:"GET",
                    headers:{
                        "content-type":"application/json"
                    }
                   

                })
                .then(res=>res.json())
                .then(data=>{
                    if(data.error)
                    {
                        this.error=data.error
                    }
                    if (data.login==="user")
                    {
                        localStorage.setItem("token",data.token)
                        this.$router.push({
                            name:"user"
                        })
                        .catch(error=>{
                        console.log(error);
                    })

                    }
                    else if(data.login=="admin")
                    {
                        localStorage.setItem("token",data.token)
                        this.$router.push({
                            name:"admin"
                        })
                        .catch(error=>{
                            console.log(error);
                    })
                    }
                })
            }
        }

    },
    created() {
        localStorage.removeItem('token')
        console.log("Logged out")
  
}
}
</script>

<style>
    .background-image-container2{
        display: flex;
        justify-content: center;
        align-items: center;
        background-image: url('./../assets/lbg.jpg'); 
        background-size: cover;
        background-position: center;
        height: 100vh;
    }
        .mainlg{
            display: flex;
            width: 537px;
            height: 288px;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            margin-top: 50px;
            margin-left: 825px;
         
        }
        .childlg1{
            display: flex;
            justify-content: space-between;
        }
        
        input{
            
            width: auto;
        }


</style>