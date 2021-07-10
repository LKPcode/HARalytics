<template>
  <div id="chart">
    <div class="row text-center font-weight-bold">
  <div class="col-sm">Max-Min: {{max_min}} </div>
  <div class="col-sm">Cacheability: {{cacheability}} </div>
 
</div>
    <apexchart
      ref="chart"
      type="bar"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>

      Content Types
      <multiselect v-model="selections.content_types.value" :options="selections.content_types.options" :multiple="true" :close-on-select="false"></multiselect>
        ISPs
      <multiselect v-model="selections.isps.value" :options="selections.isps.options" :multiple="true" :close-on-select="false"></multiselect>

      <button class="btn btn-success btn-block mt-2" @click="filter(selections)">Filter</button>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import Multiselect from 'vue-multiselect'


export default {
  name: "HeaderAnalysis",
  components: {
    apexchart: VueApexCharts,
    Multiselect
  },
  data() {
    return {
      max_min:0,
      cacheability:0,
      selections:{
       
        content_types:{
          value:null,
          options: ['list', 'of', 'font/woff2']
        },
        isps:{
          value:null,
          options: ["Wind"]
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
          categories: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        },
      },
    };
  },
  methods:{
    filter(filters){
      console.log("filters: ", filters)
      this.$axios
      .post("http://127.0.0.1:5000/header-analytics",filters, {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response header",res.data);
        let series = [{
          name: "Age",
          data: res.data.ttl.amount
        }]
        let chartOptions = {
              xaxis :  {
                  categories: res.data.ttl.age,
                
                }
            }
       
        
    
        this.chartOptions = chartOptions
        this.series = series
        this.max_min = res.data.max_min
        this.cacheability = res.data.cacheability

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

      })
      .catch((err) => console.log(err.response)); 
  },
    },
  mounted(){
        console.log("mounted scatter chart")
        this.filter(this.selections)
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