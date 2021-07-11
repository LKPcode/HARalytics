<template>
  <div id="chart">
    <apexchart v-if="loaded" type="pie" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>


<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "PieChartContent",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      loaded: false,
      series: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      chartOptions: {
         title: {
          text: "Number of Requests per Content-Type",
          align: "center",
        },
        chart: {
          width: 380,
          type: "pie",
        },
        labels: [1,2,3,4,5,6,7],
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
  mounted(){
        console.log("mounted pie chart content type")
     this.$axios
      .get("http://127.0.0.1:5000/content-type", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response types",res.data);
        this.series =  res.data.entries
        this.chartOptions = {
              labels : res.data.types,
            }
        this.loaded = true
       
      })
      .catch((err) => console.log(err.response));


  }
};
</script>