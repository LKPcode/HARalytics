<template>
  <div id="container">
    <div id="mapContainer"></div>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet.heat/dist/leaflet-heat.js";

export default {
  name: "Map",
  data() {
    return {
      center: [37, 7],
    };
  },
  methods: {
    setupLeafletMap: function (data) {
      const map = L.map("mapContainer").setView(this.center, 1);
      L.tileLayer(
        "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
        {
          attribution:
            'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          maxZoom: 18,
          id: "mapbox/streets-v11",
          tileSize: 512,
          zoomOffset: -1,
          accessToken:
            "pk.eyJ1Ijoic3BlY3RhdG9yc3MiLCJhIjoiY2tpMGRoNXp4MWM1ajJ4bXAzOTE4czAyZiJ9.nw6IW0ezv3-zU8BixQxUcg",
        }
      ).addTo(map);

      L.heatLayer(data, { radius: 15, maxZoom: 3, max: 1 }).addTo(map);
    },
  },
  mounted() {
    this.$axios
      .get("http://127.0.0.1:5000/heatmap", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log(res.data);
        this.setupLeafletMap(res.data);
      })
      .catch((err) => console.log(err.response));
  },
};
</script>

<style scoped>
#container {
  height: 500px;
}
#mapContainer {
  width: 100%;
  height: 100%;
}
</style>