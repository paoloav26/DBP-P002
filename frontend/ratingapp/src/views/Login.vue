<template>
  <div class="container d-flex justify-content-center">
    <div class="col-lg-4">
      <p id="msg"></p>
      <form @submit.prevent="login_Firebase" id="login_form">
        <p class="h1">Login</p>
        <div class="form-group">
          <label for="exampleInputEmail1">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            aria-describedby="emailHelp"
            placeholder="Enter email"
            name="email"
            v-model="email"
          />
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="Password"
            name="password"
            v-model="password"
          />
        </div>
        <label for="exampleInput"><a href="/register">Register here!</a></label>
        <button type="submit" class="btn btn-primary float-right">
          Submit
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import router from "@/router";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    login_Firebase() {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.$data.email, this.$data.password)
        .then((data) => {
          console.log(data);
          router.push({ name: "home" });
        })
        .catch((err) => alert(err.message));
    },
  },
};
</script>

<style scoped></style>
