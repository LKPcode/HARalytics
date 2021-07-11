<template>
  <l-map style="height: 600px" :zoom="zoom" :center="center" v-if="show">
    <l-tile-layer :url="url"></l-tile-layer>

    <div v-for="user in data" :key="'polyline' + user.user.email">
      <l-polyline
        v-for="server in user.servers"
        :key="'polyline' + user.user.email + server.serverIPAddress"
        :lat-lngs="[
          [user.user.ip_x, user.user.ip_y],
          [server.server_x, server.server_y],
        ]"
        :color="server.color"
        :weight="server.count"
      ></l-polyline>

      <l-circle-marker
        v-for="server in user.servers"
        :key="'marker' + server.serverIPAddress"
        :lat-lng="[server.server_x, server.server_y]"
        :radius="circle.radius"
        color="blue"
        fillColor="blue"
        :fillOpacity="1.0"
      >
        <l-tooltip>
          City: {{ server.server_city }} <br />
          <!-- Domain: {{ server.domain }} -->
        </l-tooltip>
      </l-circle-marker>
    </div>
    <l-circle-marker
      v-for="user in data"
      :key="user.user.email"
      :lat-lng="[user.user.ip_x, user.user.ip_y]"
      :radius="circle.radius"
      color="red"
      fillColor="red"
      :fillOpacity="1.0"
    >
      <l-tooltip>
        City: {{ user.user.ip_city }} <br />
        User: {{ user.user.email }}
      </l-tooltip>
    </l-circle-marker>
  </l-map>
</template>

<script>
import {
  LMap,
  LTileLayer,
  LCircleMarker,
  LPolyline,
  LTooltip,
} from "vue2-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LCircleMarker,
    LPolyline,
    LTooltip,
  },
  data() {
    return {
      url:
        "https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg",
      zoom: 3,
      center: [47.31322, -1.319482],
      circle: {
        centers: [
          [47.41322, -1.0482],
          [39.616668701171875, 19.91659927368164],
        ],
        radius: 6,
        color: "red",
      },
      polyline: {
        latlngs: [
          [47.41322, -1.0482],
          [39.616668701171875, 19.91659927368164],
        ],
        color: "#666666",
      },
      show: true,
      data: [],
    };
  },
  created() {
    this.$axios
      .get("http://127.0.0.1:5000/server_graph", {
        headers: {
          Authorization: `Token ${this.$store.token}`,
        },
      })
      .then((res) => {
        console.log("graph server", res.data);

        this.data = res.data;
      })
      .catch((err) => console.log(err.response));
  },
};
</script>
