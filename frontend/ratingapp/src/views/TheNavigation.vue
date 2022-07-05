<template>
  <div>
    <nav class="navbar navbar-dark bg-dark justify-content-between">
      <div>
        <h3 class="title">Rating app</h3>
      </div>
      <div style="display: flex; flex-direction: row">
        <div id="login_nav">
          <router-link id="login" class="text" v-bind:to="{ name: 'login' }"
            >Login</router-link
          >
          <a href="/" id="logout" class="invisible" @click.prevent="Logout"
            >Logout</a
          >
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import router from "@/router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";

export default {
  name: "TheNavigation",
  setup() {
    firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        document.getElementById("logout").className = "text";
        document.getElementById("login").className = "invisible";
      }
    });
  },
  methods: {
    Logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          router.push({ name: "home" });
          console.log("logout");
        })
        .catch((err) => alert(err.message));
    },
  },
};
</script>

<style>
.text {
  color: white;
}
.invisible {
  display: none;
}
.title {
  padding: 0;
  margin: 0;
  color: white;
}

.title:hover {
  animation: rainbow 2.5s linear;
  animation-iteration-count: infinite;
}

@keyframes rainbow {
  100%,
  0% {
    color: rgb(255, 255, 255);
  }
  2% {
    color: rgb(248, 142, 142);
  }
  4% {
    color: rgb(255, 0, 0);
  }
  8% {
    color: rgb(255, 127, 0);
  }
  16% {
    color: rgb(255, 255, 0);
  }
  25% {
    color: rgb(127, 255, 0);
  }
  33% {
    color: rgb(0, 255, 0);
  }
  41% {
    color: rgb(0, 255, 127);
  }
  50% {
    color: rgb(0, 255, 255);
  }
  58% {
    color: rgb(0, 127, 255);
  }
  66% {
    color: rgb(0, 0, 255);
  }
  75% {
    color: rgb(127, 0, 255);
  }
  83% {
    color: rgb(255, 0, 255);
  }
  91% {
    color: rgb(255, 0, 127);
  }
}
</style>
