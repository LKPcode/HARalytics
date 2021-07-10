<template>
  <div>
    <nav-bar />
    <div class="container content">
<div class="row text-center font-weight-bold">
  <div class="col-sm">Users: {{general.count_users}} </div>
  <div class="col-sm">Providers: {{general.count_providers}} </div>
  <div class="col-sm">Domains: {{general.count_domains}} </div>
</div>


      <div class="row">
        <div class="col-sm card m-3 p-3">
          <column-chart />
        </div>
        <div class="col-sm card m-3 p-3">
          <pie-chart />
        </div>
      </div>
      <div class="row">
        <div class="col-sm card m-3 p-3">
         <pie-chart-content/>
        </div>
      </div>
      <div class="row">
        <div class="col-sm card m-3 p-3">
          <scatter-chart />
        </div>
      </div>
      <div class="row">
        <div class="col-sm card m-3 p-3">
          <header-analysis/>
        </div>
      </div>
      <div class="row">
        <div class="col-sm card m-3 p-4">
          <server-map />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ColumnChart from "../components/ColumnChart.vue";
import ScatterChart from "../components/ScatterChart.vue";
import ServerMap from "../components/ServerMap.vue";
import NavBar from "../components/NavBar.vue";
import PieChart from "../components/PieChart.vue";
import PieChartContent from "../components/PieChartContentType.vue";
import HeaderAnalysis from "../components/HeaderAnalysis.vue"

export default {
  name: "Admin",
  components: {
    ColumnChart,
    ScatterChart,
    ServerMap,
    NavBar,
    PieChart,
    PieChartContent,
    HeaderAnalysis
  },
  data(){
    return{
      general: {
        count_users: 0,
        count_domains: 0,
        count_providers: 0
      }
    }
  },
  created(){

  },
  mounted(){
     this.$axios
      .get("http://127.0.0.1:5000/general", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("response",res.data);
        this.general = res.data
      })
      .catch((err) => console.log(err.response));

      if(this.$store.state != "admin"){
        this.$router.go(-1)
      }
      
  }
};
</script>

<style scoped>
.map {
  height: 600px;
}
.content {
  padding-top: 100px;
}
</style>