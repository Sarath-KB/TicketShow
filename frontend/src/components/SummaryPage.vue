<template>
<div>
  <div  style ="margin: auto;text-align: center;">
    <h1>Summary Page </h1></div>
    <div>
    <GChart
    type="ColumnChart"
    :data="chartData"
    :options="chartOptions"
  />
    <!-- <SummaryPage2  id="{{this.vid}}"/> -->
        <div>
    <button class="btn" @click="exportToCSV">Download CSV</button>
  </div>
</div>
</div>

   
</template>

<script>

import { GChart } from 'vue-google-charts';
// import SummaryPage2 from './components/SummaryPage2.vue'
// import { saveAs } from 'file-saver';
// import { stringify } from 'csv-stringify';
import Papa from 'papaparse';
export default {
    name:'SummaryPage',
    components: {
        GChart,
        // SummaryPage2
    },
    props:{
    id:{
        type:[Number,String],
        required:true
        }
    },
    data(){
    return {
        showdata:[],
        vid: null,
        chartData: [],
        chartOptions: {
        chart: {
        title: 'List summary',
        trendlines: { 0: {} } 
        }
    }  
    }  
    },
    methods:{
            summary(){
            fetch(`http://127.0.0.1:5000/showlist/${this.vid}`,{
            method:"GET",
            headers:{
                "content-type":"application/json",
            }
        })
        .then(res=>res.json())
        .then(data=>{
            
            this.showdata.push(...data.data)
            console.log(this.showdata);
            var ks = this.showdata;
             let lp=['List','Ticket Sold']
                let ls=[]
       ls.push(lp)
        for (var k of ks) 
            {
            let temp=[]
            temp.push(k.show_name)
            temp.push(parseInt(k.tickets_sold))

            ls.push(temp)
            console.log("ls list=",ls)
            }
// console.log("chart data=:",this.chartData);
// console.log("ls list=",ls)

this.chartData=ls;
        })
        .catch(error=>{
            console.log(error);
        })

        },
    exportToCSV() {
      const csv = Papa.unparse(this.showdata);
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'exported_data.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    },

    
    created(){
        this.vid=this.$route.params.id
        this.summary()
        
    }


}

</script>

<style>

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
</style>