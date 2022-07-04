import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/categorias/:categoria",
    name: "categorias",
    props: true,
    component: () =>
      import(/* webpackChunkName: "Categorias" */ "../views/Categorias.vue"),
  },
  {
    path: "/categorias/:categoria/item/:item",
    name: "item",
    props: true,
    component: () => import(/* webpackChunkName: "item" */ "../views/Item.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/Register.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
