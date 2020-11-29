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
          data: [21, 22, 10, 28, 16],
        },
      ],
      chartOptions: {
        title: {
          text: "Product Trends by Month",
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
            ["John", "Doe"],
            ["Joe", "Smith"],
            ["Jake", "Williams"],
            "Amber",
            ["Peter", "Brown"],
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
};
</script>