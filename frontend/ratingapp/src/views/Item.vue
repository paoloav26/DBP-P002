<template>
  <the-navigation />
  <div class="item_display">
    <h1 style="margin-bottom: 15px">{{ item_data.nombre }}</h1>
    <div class="image_description_container">
      <img
        class="item_image_display"
        v-bind:src="require(`@/assets/${item_data.imagen}`)"
      />
      <div style="display: flex; flex-direction: column; padding-left: 1%">
        <h2>Description:</h2>
        <p1 style="font-size: large">{{ item_data.descripcion }}</p1>
        <br />
        <h4>Calificación: {{ item_data.calificacion }}⭐</h4>
        <from>
          <h4>Tu Calificacion</h4>
          <div id="puntaje" style="display: inline">
            <fieldset id="campo">
              <label>
                <input
                  type="radio"
                  name="number"
                  value="1"
                  v-model="puntaje"
                />1⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="number"
                  value="2"
                  v-model="puntaje"
                />2⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="number"
                  value="3"
                  v-model="puntaje"
                />3⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="number"
                  value="4"
                  v-model="puntaje"
                />4⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="number"
                  value="5"
                  v-model="puntaje"
                />5⭐
              </label>
            </fieldset>
          </div>

          <p id="coment_msg"></p>
          <h4>Tu Comentario:</h4>
          <div>
            <textarea
              name="comentario"
              rows="10"
              cols="70"
              id="comentario"
              v-model="comentario"
            ></textarea>
            <br />
          </div>
          <div v-if="this.$data.comentarioi == ''">
            <input
              type="button"
              value="Subir Calificacion"
              id="subir"
              style="margin-top: 15px"
              @click.prevent="postCalificacion"
            />
          </div>
          <div v-else>
            <input
              type="button"
              value="Eliminar Comentario"
              id="eliminar"
              style="margin: 15px 0px 10px 10px"
              class=""
            />
            <a href="/actualizar_comentario/{{item.id}}">
              <input
                type="button"
                value="Actualizar Comentario"
                id="actualizar"
                style="margin: 15px 0px 10px 10px"
                class=""
                @click.prevent="patchCalificacion"
              />
            </a>
          </div>
        </from>
        <h4>Comentarios:</h4>
        <div id="box_container">
          <div
            v-for="comentario in comentarios"
            v-bind:key="comentario.username"
            class="card"
          >
            <div class="card-body">
              <h5 class="card-title">{{ comentario.username }}</h5>
              <p class="card-text">{{ comentario.comentario }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  {{ comentario }}
  <nologinreturn />
</template>

<script>
import TheNavigation from "./TheNavigation.vue";
import Nologinreturn from "@/components/Nologinreturn.vue";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";

export default {
  name: "Item",
  data() {
    return {
      items: "",
      item_id: this.$route.params.item,
      categoria: this.$route.params.categoria,
      comentarios: "",
      user: "",
      comentario: "",
      comentarioi: "",
      puntaje: "",
    };
  },
  computed: {
    item_data() {
      return this.$data.items.find((t) => t.id == this.$data.item_id);
    },
  },
  created() {
    this.getItems();
    this.getComentarios();
    this.getUser();
    this.getComentario();
  },
  methods: {
    getItems() {
      fetch(
        "http://127.0.0.1:5000/items?categoria=" + this.$route.params.categoria,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.items = data.items;
        });
    },
    getComentarios() {
      fetch(
        "http://127.0.0.1:5000/calificaciones?item=" + this.$route.params.item,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.comentarios = data.calificaciones;
        });
    },
    getComentario() {
      fetch(
        "http://127.0.0.1:5000/calificaciones?item=" + this.$route.params.item,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.$data.comentario = data.calificaciones.find(
            (t) => t.username == this.$data.user.username
          );
          this.$data.comentario = this.$data.comentario.comentario;

          this.$data.comentarioi = data.calificaciones.find(
            (t) => t.username == this.$data.user.username
          );
          this.$data.comentarioi = this.$data.comentario.comentarioi;
        });
    },
    getUser() {
      const user = firebase.auth().currentUser;
      fetch("http://127.0.0.1:5000/usuarios", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.user = data.usuarios.find((t) => t.correo == user.email);
        });
    },
    postCalificacion() {
      fetch("http://127.0.0.1:5000/calificaciones", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          usuario_username: this.$data.user.username,
          items_id: this.$data.item_id,
          puntaje: this.$data.puntaje,
          comentario: this.$data.comentario,
        }),
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          console.log(data);
          this.$data.comentarioi = this.$data.comentario;
        });
    },
    patchCalificacion() {
      fetch(
        "http://127.0.0.1:5000/calificaciones/" +
          this.$data.user.username +
          "/" +
          this.$data.item_id,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            puntaje: this.$data.puntaje,
            comentario: this.$data.comentario,
          }),
        }
      )
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          console.log(data);
          this.$data.comentarioi = this.$data.comentario;
          this.$data.comentarioi = this.$data.comentario;
        });
    },
  },
  components: { TheNavigation, Nologinreturn },
};
</script>

<style>
.item_display {
  padding: 3%;
}

.item_image_display {
  height: 70%;
  width: 25%;
}

.image_description_container {
  display: flex;
  flex-direction: row;
}
</style>
