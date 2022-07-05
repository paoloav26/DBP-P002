<template>
  <title>{{ categoria }}</title>
  <the-navigation />
  <div>
    <div id="items_list" class="items_list">
      <div class="item" v-for="item in items" v-bind:key="item.id">
        <router-link v-bind:to="{ name: 'item', params: { item: item.id } }">
          <img
            class="item_image"
            v-bind:src="require(`@/assets/${item.imagen}`)"
          />
          <h4 class="item_titulo">{{ item.nombre }}</h4>
        </router-link>
      </div>
    </div>
  </div>
  <nologinreturn />
</template>

<script>
import TheNavigation from "./TheNavigation.vue";
import Nologinreturn from "@/components/Nologinreturn.vue";

export default {
  data() {
    return {
      items: this.getItems(),
    };
  },
  props: {
    categoria: {
      type: String,
      required: true,
    },
  },
  methods: {
    getItems() {
      fetch("http://127.0.0.1:5000/items?categoria=" + this.categoria, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.items = data.items;
        });
    },
  },
  computed: {},
  components: { TheNavigation, Nologinreturn },
};
</script>

<style>
.items_list {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
}

.item {
  padding: 20px;
  text-align: center;
}

.item_image {
  height: 400px;
}

.item_titulo {
  padding-top: 10px;
}
</style>
