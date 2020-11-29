<template>
  <div>
    <nav-bar />
    <div class="container">
      <div class="row">
        <div class="col-sm card m-3 p-3">
          <h2 class="text-center">256</h2>
        </div>
        <div class="col-sm card m-3"></div>
      </div>

      <div class="row">
        <div class="col-sm card m-3">
          <heatmap />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar.vue";
import Heatmap from "../components/Heatmap.vue";

export default {
  name: "Admin",
  components: {
    Heatmap,
    NavBar,
  },
};
</script>

<style scoped>
.container {
  padding-top: 60px;
}
</style>