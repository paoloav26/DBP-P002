<template>
  <div class="home">
    <div class="page-wrap d-flex flex-row align-items-center">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-12 text-center">
            <span class="display-1 d-block">Bienvenido!, {{ name }}</span>
            <div class="mb-4 subtitulo">A continuación elige una categoría</div>
            <category-selector />
          </div>
          <button class="logout" @click="Logout">Logout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import CategorySelector from "../components/CategorySelector";
import { ref, onBeforeMount } from "vue";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
export default {
  name: "Home",
  components: { CategorySelector },
  setup() {
    const name = ref("");
    onBeforeMount(() => {
      const user = firebase.auth().currentUser;
      if (user) {
        name.value = user.email.split("@")[0];
      }
    });
    const Logout = () => {
      firebase
        .auth()
        .signOut()
        .then(() => console.log("Signed out"))
        .catch((err) => alert(err.message));
    };
    return {
      name,
      Logout,
    };
  },
};
</script>

<style>
.subtitulo {
  font-size: 20px;
}
</style>
