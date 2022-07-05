<template>
  <div class="container d-flex justify-content-center">
    <div class="col-lg-4">
      <p id="msg"></p>
      <form @submit.prevent="firebase_Register" id="register_form">
        <p class="h1">Register</p>
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
        <div class="form-group">
          <label for="exampleInputPassword1">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="Username"
            name="username"
            v-model="username"
          />
        </div>
        <label for="exampleInput"><a href="/login">Login here!</a></label>
        <button type="submit" class="btn btn-primary float-right">
          Submit
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  methods: {
    firebase_Register() {
      firebase
        .auth()
        .createUserWithEmailAndPassword(this.$data.email, this.$data.password)
        .then((user) => {
          console.log(user);
          router.push({ name: "home" });
        })
        .catch((err) => alert(err.message));
    },
  },
};
</script>

<style scoped>
li {
  list-style: none;
}
</style>
