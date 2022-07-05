import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBbykj14XVqqbwWN9sAR6dxsc-4ANiKeIs",
  authDomain: "dbp-rating-app.firebaseapp.com",
  projectId: "dbp-rating-app",
  storageBucket: "dbp-rating-app.appspot.com",
  messagingSenderId: "197968183325",
  appId: "1:197968183325:web:693546bb6fd02d731c86f4",
};

firebase.initializeApp(firebaseConfig);

createApp(App).use(router).mount("#app");
