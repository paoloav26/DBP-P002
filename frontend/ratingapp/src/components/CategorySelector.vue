<template>
  <select @change="onChange($event)">
    <option disabled selected>Categorias</option>
    <option v-for="categoria in categorias" v-bind:key="categoria.categoria">
      {{ categoria.categoria }}
    </option>
  </select>
</template>

<script>
export default {
  name: "CategorySelector",
  data() {
    return {
      categorias: "",
    };
  },
  created() {
    this.getCategorias();
  },
  methods: {
    onChange(e) {
      this.$router.push({
        name: "categorias",
        params: { categoria: e.target.value },
      });
    },
    getCategorias() {
      fetch("http://127.0.0.1:5000/categorias", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          this.categorias = data.categorias;
        });
    },
  },
};
</script>
