<template>
  <select @change="onChange(this.value)">
    <option disabled selected>Categorias</option>
    <option value="/categoria">categoria</option>
  </select>
</template>

<script>
export default {
  name: "CategorySelector",
  methods: {
    onChange(value) {
      window.location.href = value;
    },
  },
};
</script>
