<template>
  <div id="chart">
    <apexchart
      ref="chart"
      type="line"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>

        Methods
      <multiselect v-model="selections.methods.value" :options="selections.methods.options" :multiple="true" :close-on-select="false"></multiselect>
        Content Types
      <multiselect v-model="selections.content_types.value" :options="selections.content_types.options" :multiple="true" :close-on-select="false"></multiselect>
        weekdays
      <multiselect v-model="selections.weekdays.value" :options="selections.weekdays.options" :multiple="true" :close-on-select="false"></multiselect>
        ISPs
      <multiselect v-model="selections.isps.value" :options="selections.isps.options" :multiple="true" :close-on-select="false"></multiselect>

      <button class="btn btn-success btn-block mt-2" @click="filter(selections)">Filter</button>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import Multiselect from 'vue-multiselect'


export default {
  name: "Timings",
  components: {
    apexchart: VueApexCharts,
    Multiselect
  },
  data() {
    return {
      selections:{
        methods:{
          value:null,
          options: ['list', 'of', 'options']
        },
        content_types:{
          value:null,
          options: ['list', 'of', 'options']
        },
        weekdays:{
          value:null,
          options: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        },
        isps:{
          value:null,
          options: ['list', 'of', 'options']
        }
      },
      series: [
        {
          name: "Age",
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        },
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: "line",
          zoom: {
            enabled: false,
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: "straight",
        },
        title: {
          text: "Product Trends by Month",
          align: "center",
        },
        grid: {
          row: {
            colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
            opacity: 0.5,
          },
        },
        xaxis: {
          categories: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        },
      },
    };
  },
  methods:{
    filter(filters){
      this.$axios
      .post("http://127.0.0.1:5000/timings",filters, {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response",res.data);
        let series = [{
          name: "Age",
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }]
        
       
        for(let i=0; i<res.data.length; i++){
          series[0].data[res.data[i].hours] = res.data[i].time;
        }
    
     
       this.series = series
    

      })
      .catch((err) => console.log(err.response)); 
    },
      fillOptions(){
     this.$axios
      .get("http://127.0.0.1:5000/all-options",{
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response options",res.data);
        this.selections.content_types.options = res.data.content_type
        this.selections.isps.options = res.data.ISP
        this.selections.methods.options = res.data.method



      })
      .catch((err) => console.log(err.response)); 
  },
  },
  mounted(){
        console.log("mounted scatter chart")
        this.filter(this.selections)
        this.selections.methods.options = ["ok", "not ok", "whatever"]
        this.fillOptions()
       
     

    
    
  }

 
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
.sortMenu {
  padding: 3px;
  display: flex;
  justify-content: space-around;
}
.title {
  font-size: 14px;
}
.btn-bg {
  background-color: var(--secondary-bg-color);
}
</style>