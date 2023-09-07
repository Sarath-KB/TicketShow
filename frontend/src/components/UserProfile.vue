<template>
<div class="prof">
    <h1>User:{{username}}</h1>
    <div v-for =" venue in venuelist " :key="venue.id">

  <div class="mainup" v-if="checkIfIdExists(venue.id)">
    <br/>
        
        <div class="subup"  v-for ="book in booklist" :key="book.id" >
            <div v-if="book.venue_id==venue.id">
                <div class="ven"><u>Venue:{{venue.name}}</u></div>
                <div class="childup1">

                    <div style="margin-top:-5px;margin-left: 10px;"><h2> Name:{{book.showname}}<br/>Tag:{{book.tag}}<br/>Time:{{book.timing}} <br/></h2>
                    </div>
                </div>
              
            </div>     
        
        
        
<br/>
</div>
            </div>
</div>
</div>


</template>

<script>
export default {
    name:'UserProfile',
    data(){
        return{
            venuelist:[],
            booklist:[],
            username:null,
            token:null,
            checklist:[]
    }
    },
    methods:{
        getvenue(){
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
            
        })
        .catch(error=>{
            console.log(error);
        })
            
        },
        getuser()
        {
        fetch('http://127.0.0.1:5000/getuser',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token": this.token
            }
        })
        .then(resp=>resp.json())
        .then(data=>{
            console.log(data)
            this.username=data.data[0].name
        })
        .catch(error=>{
            console.log(error);
        })

        },


        getbooking()
        {
            console.log(this.token);
        fetch('http://127.0.0.1:5000/getbooking',{
            method:"GET",
            headers:{
                "content-type":"application/json",
                "x-access-token": this.token
            }
        })
        .then(resp=>resp.json())
        .then(data=>{
            this.booklist.push(...data.data)
            this.checklist.push(...data.vd)
        })
        .catch(error=>{
            console.log(error);
        })

        },
        
         checkIfIdExists(idToCheck) {

        // console.log(idToCheck)
      // Method to check if the id exists in the JSON array
        return this.booklist.some(item => item.venue_id === idToCheck);
    }

    },
    created(){
        this.token = localStorage.getItem('token')
        console.log(this.token)
        this.getbooking()
        
        this.getuser()
        this.getvenue()
}
}
</script>

<style>

        .ven{
            font-size: 30px;
            margin-left: 10px;
            margin-top:10px;
            font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
        }
        .prof{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            
        }
        .mainup{
            display: flex;
            border: black solid 2px;
            /* background-color:#ADD8E6;
            border-radius: 10px; */
            height: 250px;
            width:800px;
            margin-left: 250px;
            margin-right: 30px;
            
        } 
        .subup{
            display: flex;
        }
         
        .childup1{
            display: flex;
            padding:auto;
            margin-left: 50px;
        }
            .btn {
            background-color: white; 
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            color:black;
        }
</style>