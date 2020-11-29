<template>
  <div>
    <nav-bar />
    <div class="container content">
      <div class="row">
        <div class="col-sm card m-3 p-3">
          <column-chart />
        </div>
        <div class="col-sm card m-3 p-3">
          <scatter-chart />
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

export default {
  name: "Admin",
  components: {
    ColumnChart,
    ScatterChart,
    ServerMap,
    NavBar,
  },
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