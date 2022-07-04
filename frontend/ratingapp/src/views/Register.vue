<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="Register">
      <ul>
        <li>
          <input type="text" placeholder="Username" v-model="username" />
        </li>
        <li>
          <input type="text" placeholder="Email" v-model="email" />
        </li>
        <li>
          <input type="password" placeholder="Password" v-model="password" />
        </li>
        <li>
          <input type="submit" value="Register" />
        </li>
      </ul>
      <p>Have an account? <router-link to="/login">Login Here</router-link></p>
    </form>
  </div>
</template>

<script>
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import { ref } from "vue";

export default {
  setup() {
    const username = ref("");
    const email = ref("");
    const password = ref("");
    const Register = () => {
      firebase
        .auth()
        .createUserWithEmailAndPassword(
          username.value,
          email.value,
          password.value
        )
        .then((user) => {
          alert(user);
        })
        .catch((err) => alert(err.message));
    };
    return {
      Register,
      username,
      email,
      password,
    };
  },
};
</script>

<style scoped>
li {
  list-style: none;
}
</style>
