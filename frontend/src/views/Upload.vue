<template>
  <div class="about">
    <nav-bar />
    <div class="uploadArea">
      <div>
        <h4>Select a HAR file for Upload.</h4>
        <h6>{{ filename }}</h6>
        <label class="label onHover"
          ><input
            hidden
            type="file"
            @change="loadTextFromFile"
            class="hidden"
            accept=".har"
          />
          <div v-if="!processing">
            Select <span v-if="processed">Another</span> File
          </div>
          <div v-else class="loader"></div>
        </label>

        <div v-if="processed" class="buttons">
          <div @click="uploadJson()" class="uploadFile onHover">
            Upload File
          </div>

          <div @click="saveFile()" class="saveBtn onHover">Save file</div>
        </div>
      </div>
    </div>
    <div class="infoArea">
      <div class="">
        <json-view :data="json" class="customize" />
      </div>
    </div>
  </div>
</template>

<script>
import { JSONView } from "vue-json-component";
import NavBar from "../components/NavBar.vue";

export default {
  components: {
    "json-view": JSONView,
    NavBar,
  },
  data() {
    return {
      json: {},
      original: {},
      headers: {},
      processing: false,
      processed: false,
      filename: "",
      token: this.$store.token,
    };
  },
  methods: {
    saveFile: function () {
      const data = JSON.stringify(this.json);
      const blob = new Blob([data], { type: "text/plain" });
      const e = document.createEvent("MouseEvents"),
        a = document.createElement("a");
      a.download = "test.json";
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
      e.initEvent(
        "click",
        true,
        false,
        window,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      );
      a.dispatchEvent(e);
    },
    changeHeadersStructure(headers) {
      let new_headers = {
        content_type: "",
        cache_control: "",
        pragma: "",
        expires: "",
        age: "",
        last_modified: "",
        host: "",
      };

      for (let index in headers) {
        if (headers[index].name == "content-type") {
          new_headers.content_type = headers[index].value;
        } else if (headers[index].name == "cache-control") {
          new_headers.cache_control = headers[index].value;
        } else if (headers[index].name == "pragma") {
          new_headers.pragma = headers[index].value;
        } else if (headers[index].name == "expires") {
          new_headers.expires = headers[index].value;
        } else if (headers[index].name == "age") {
          new_headers.age = headers[index].value;
        } else if (headers[index].name == "last_modified") {
          new_headers.last_modified = headers[index].value;
        } else if (headers[index].name == "host") {
          new_headers.host = headers[index].value;
        }
      }
      return new_headers;
    },
    uploadJson() {
      this.$axios
        .post("http://127.0.0.1:5000/upload", this.json, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        })
        .then((res) => {
          console.log(res.data);
          if (this.$store.state == "admin") {
            this.$router.push("/admin");
          } else {
            this.$router.push("/user");
          }
        })
        .catch((err) => console.log(err.response));
    },

    loadTextFromFile(ev) {
      this.processing = true;

      const file = ev.target.files[0];

      const reader = new FileReader();

      reader.onload = (e) => {
        this.original = JSON.parse(e.target.result);

        let entries = JSON.parse(e.target.result).log.entries;

        let new_json = [];

        for (let index in entries) {
          console.log(entries[index]);
          new_json.push({
            serverIPAddress: entries[index].serverIPAddress,
            startedDateTime: entries[index].startedDateTime,
            timings: entries[index].timings.wait,
            method: entries[index].request.method,
            url: entries[index].request.url,
            ReqHeaders: this.changeHeadersStructure(
              entries[index].request.headers
            ),
            status: entries[index].response.status,
            statusText: entries[index].response.statusText,
            ResHeaders: this.changeHeadersStructure(
              entries[index].response.headers
            ),
          });
        }

        let headers = {};
        console.log("yoyo");

        this.headers = headers;

        this.json = { new_json };

        this.filename = file.name;

        this.processing = false;
        this.processed = true;

        // for (let entry of this.json.entries) {
        //   console.log(entry); // Will display contents of the object inside the array
        // }
      };
      reader.readAsText(file);
    },
  },
};
</script>

<style scoped>
h4,
h6 {
  color: white;
  margin-bottom: 40px;
}
.about {
  display: flex;
  height: 100%;
  text-align: center;
}
.uploadArea {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 40%;
  background-color: var(--main-bg-color);
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
}
.infoArea {
  height: 100%;
  width: 60%;
  overflow: auto;
  padding-top: 58px;
}
.label {
  background-color: var(--secondary-bg-color);
  padding: 16px;
  margin-bottom: 10px;
  border-radius: 10px;
  width: 100%;
}
.file {
  margin: auto;
  height: 100%;
  width: 100%;
}
.saveBtn {
  background-color: var(--secondary-bg-color);
  padding: 20px;
  margin-left: 10px;
  margin-top: 10px;
  border-radius: 10px;
  width: 50%;
}
.uploadFile {
  background-color: var(--secondary-bg-color);
  padding: 20px;
  margin-right: 10px;
  margin-top: 10px;
  border-radius: 10px;
  width: 50%;
}
.buttons {
  display: flex;
}
.onHover:hover {
  background-color: var(--space-bg-color);
  cursor: pointer;
}

.customize {
  --vjc-valueKey-color: green;
}
.customize.dark {
  --vjc-valueKey-color: red;
}

.loader {
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 1s linear infinite;
  margin: auto;
}

/* Safari */
@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>