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
    name: "login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue"),
  },
  {
    path: "/logout",
    name: "logout",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
