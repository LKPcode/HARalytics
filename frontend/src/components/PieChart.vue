<template>
  <div id="chart">
    <apexchart v-if="loaded" type="pie" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>


<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "PieChart",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      loaded: false,
      series: [1,1,1,1,1],
      chartOptions: {
        colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0'],
         title: {
          text: "Number of Requests per Response code",
          align: "center",
        },
        chart: {
          width: 380,
          type: "pie",
        },
        labels: [],
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: 200,
              },
              legend: {
                position: "bottom",
              },
            },
          },
        ],
      },
    };
  },
  created(){
        console.log("mounted pie chart")
     this.$axios
      .get("http://127.0.0.1:5000/status", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response",res.data);
        this.series =  res.data.entries
        this.chartOptions = {
              labels : res.data.statuses,
              
            }
        this.loaded = true


      })
      .catch((err) => console.log(err.response));


  }
};
</script>