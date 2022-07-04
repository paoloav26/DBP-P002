<template>
  <link
    rel="stylesheet"
    type="text/css"
    href="{{ url_for('static',filename='styles.css') }}"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
    crossorigin="anonymous"
  />

  <the-navigation />
  <router-view :key="$route.path" />
</template>

<script>
import { onBeforeMount } from "vue";
import TheNavigation from "./views/TheNavigation.vue";
import { useRouter, useRoute } from "vue-router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    onBeforeMount(() => {
      firebase.auth().onAuthStateChanged((user) => {
        if (!user) {
          router.replace("/login");
        } else if (route.path == "/login" || route.path == "/register") {
          router.replace("/");
        }
      });
    });
  },
  name: "App",
  components: {
    TheNavigation,
  },
};
</script>

<style>
body {
  margin: 0;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
