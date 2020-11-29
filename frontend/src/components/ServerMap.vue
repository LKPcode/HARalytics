<template>
  <l-map style="height: 600px" :zoom="zoom" :center="center">
    <l-tile-layer :url="url"></l-tile-layer>
    <l-circle-marker
      v-for="(center, index) in circle.centers"
      :key="index"
      :lat-lng="center"
      :radius="circle.radius"
      :color="circle.color"
      :fillColor="circle.color"
      :fillOpacity="1.0"
    />
    <l-polyline
      :lat-lngs="polyline.latlngs"
      :color="polyline.color"
      :weight="5"
    ></l-polyline>
  </l-map>
</template>

<script>
import { LMap, LTileLayer, LCircleMarker, LPolyline } from "vue2-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LCircleMarker,
    LPolyline,
  },
  data() {
    return {
      url:
        "https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg",
      zoom: 6,
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
          [46.45322, -1.9582],
        ],
        color: "green",
      },
    };
  },
};
</script>
