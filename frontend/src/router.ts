import { RouteLocationNormalized } from "vue-router";
import Cookies from "js-cookie";

import HomeView from "@/views/HomeView.vue";
import AuthView from "@/views/AuthView.vue";
import VerifyCodeView from "@/views/VerifyCodeView.vue";
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { authStore } from "@/store/authStore";
import { createPinia, storeToRefs } from "pinia";

const pinia = createPinia();
const store = authStore(pinia);

const { isAuth } = storeToRefs(store);
const { getCookieAuth } = store;

const authGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (!isAuth.value) {
    next("/login");
  } else {
    next();
  }
};

const userAuth = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (isAuth.value) {
    next("/");
  } else {
    next();
  }
};

const verifyCode = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (!isAuth.value && Cookies.get("access") !== "undefined") {
    next("/");
  } else {
    next();
  }
};

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    props: {},
    // beforeEnter: authGuard,
  },
  {
    path: "/auth",
    name: "auth",
    component: AuthView,
    props: {},
    // beforeEnter: authGuard,
  },
  {
    path: "/verify-code",
    name: "verify-code",
    component: VerifyCodeView,
    props: {},
    // beforeEnter: authGuard,
  },

  {
    path: "/:pathMatch(.*)",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  getCookieAuth().then(() => {
    next();
  });
});
export default router;
