<template>
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Item",
  data() {
    return {
      items: this.getItems(),
      item_id: this.$route.params.item,
      categoria: this.$route.params.categoria,
    };
  },
  computed: {
    item_data() {
      return this.items.find((t) => t.id == this.item_id);
    },
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
  },
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
