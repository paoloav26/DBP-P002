<template>
  <div class="home">
    <div class="page-wrap d-flex flex-row align-items-center">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-12 text-center">
            <span class="display-1 d-block">Bienvenido!</span>
            <div class="mb-4 subtitulo">A continuación elige una categoría</div>
            <select>
              <option disabled selected>Categorias</option>

              <option value="/categoria">categoria</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
};
</script>

<style>
.subtitulo {
  font-size: 20px;
}
</style>
