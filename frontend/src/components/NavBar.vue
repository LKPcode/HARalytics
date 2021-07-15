<template>
  <nav
    class="navbar fixed-top navbar-expand-lg navbar-light p-0 px-2"
    style="background-color: var(--secondary-bg-color)"
  >
    <a class="navbar-brand company-name" href="#">
      <img src="../assets/logo.png" width="50" height="50" alt="" />
      HARalytics
    </a>

    <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" @click="$router.push('user')">My Data</a>
        </li>
        <li v-if="state == 'admin'" class="nav-item active">
          <a class="nav-link" @click="$router.push('admin')">General Data</a>
        </li>
        <li class="nav-item active">
          <a class="nav-link" @click="$router.push('upload')">Upload</a>
        </li>
        <li class="nav-item active">
          <a class="nav-link" @click="$router.push('update')">Update Account</a>
        </li>
      </ul>

      <button
        class="btn btn-danger my-2 my-sm-0"
        @click="logout();$router.push('/')"
        type="submit"
      >
        Log Out
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  data(){
    return{
      state: this.$store.state
    }
  },
  methods:{
    logout()
    {
      this.$store.logout()
    }
  }
};
</script>

<style scoped>
.company-name {
  font-weight: bold;
}
.nav-item {
  cursor: pointer;
}
</style>