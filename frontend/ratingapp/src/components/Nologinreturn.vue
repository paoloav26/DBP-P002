<script>
import router from "@/router";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";

export default {
  name: "NoLoginReturn",
  setup() {
    firebase.auth().onAuthStateChanged((user) => {
      if (!user) {
        router.push({ name: "home" });
        this.$router.reload();
      }
    });
  },
};
</script>
