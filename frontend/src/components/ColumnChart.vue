<template>
  <div id="chart">
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>


<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "ColumnChart",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [
        {
          data: [0,0,0,0],
        },
      ],
      chartOptions: {
        title: {
          text: "Number of Requests per Method",
          align: "center",
        },
        chart: {
          type: "bar",
          events: {
            click: function (chart, w, e) {
              console.log(chart, w, e);
            },
          },
        },
        colors: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],

        plotOptions: {
          bar: {
            columnWidth: "60%",
            distributed: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        legend: {
          show: false,
        },
        xaxis: {
          categories: [
 
          ],
          labels: {
            style: {
              colors: ["#2E93fA", "#66DA26", "#546E7A", "#E91E63", "#FF9800"],

              fontSize: "12px",
            },
          },
        },
      },
    };
  },
  mounted(){
    console.log("mounted column chart")
     this.$axios
      .get("http://127.0.0.1:5000/methods", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response",res.data);
        this.series = [{
                data: res.data.amounts,
                
            }]
        this.chartOptions = {
              xaxis :  {
                  categories: res.data.methods,
                
                }
            }


      })
      .catch((err) => console.log(err.response));


    
  }
};
</script>