<template>
  <the-navigation />
  <div class="home">
    <div class="page-wrap d-flex flex-row align-items-center">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-12 text-center">
            <span class="display-1 d-block">Bienvenido {{ name }}!</span>
            <div class="mb-4 subtitulo">A continuación elige una categoría</div>
            <category-selector />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import CategorySelector from "../components/CategorySelector";
import TheNavigation from "./TheNavigation.vue";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";
export default {
  name: "Home",
  components: { CategorySelector, TheNavigation },
  data() {
    return {
      name: this.setName().name,
    };
  },
  methods: {
    setName() {
      const user = firebase.auth().currentUser;
      let name_ = "";
      if (user) {
        name_ = user.email.split("@")[0];
      }
      return {
        name: name_,
      };
    },
  },
};
</script>

<style>
.subtitulo {
  font-size: 20px;
}
</style>
