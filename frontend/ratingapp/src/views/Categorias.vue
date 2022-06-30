<template>
  <div>
    {{ categoria }}
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoria: this.$route.params.categoria,
    };
  },
};
</script>

<style></style>
