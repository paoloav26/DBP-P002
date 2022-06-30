<template>
  <title>{{ categoria }}</title>
  <div>
    <div id="items_list" class="items_list">
      <div class="item" v-for="item in items" v-bind:key="item.id">
        <a href="">
          <img
            class="item_image"
            v-bind:src="require(`@/assets/${item.imagen}`)"
          />
          <h4 class="item_titulo">{{ item.nombre }}</h4>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoria: this.$route.params.categoria,
      items: this.getItems(),
    };
  },
  methods: {
    getItems() {
      fetch("http://127.0.0.1:5000/items", {
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
