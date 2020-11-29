<template>
  <div id="app">
    <div id="nav">
      <!-- <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> -->
    </div>
    <transition name="fade">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {};
</script>

<style>
body,
html {
  height: 100%;
  background-color: var(--space-bg-color);
}
/* body {
  padding-top: 60px;
} */
#app {
  height: 100%;
}
:root {
  --main-bg-color: #368f8b;
  --secondary-bg-color: #31da9d;
  --space-bg-color: #ffffe8;
}

@import "~bootstrap/dist/css/bootstrap.css";
</style>



