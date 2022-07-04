import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAHMFWabMhXzM7vm56HV3dwzlzh4VnB7dw",
  authDomain: "ratingapp-bd693.firebaseapp.com",
  projectId: "ratingapp-bd693",
  storageBucket: "ratingapp-bd693.appspot.com",
  messagingSenderId: "749211638150",
  appId: "1:749211638150:web:c7e96b6566bc7923853407",
};

firebase.initializeApp(firebaseConfig);

createApp(App).use(router).mount("#app");
