import { RouteLocationNormalized } from "vue-router";
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
  // @ts-ignore
  to: RouteLocationNormalized,
  // @ts-ignore
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (!isAuth.value) {
    next("/auth");
  } else {
    next();
  }
};

const userAuth = async (
  // @ts-ignore
  to: RouteLocationNormalized,
  // @ts-ignore
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (isAuth.value) {
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
    beforeEnter: authGuard,
  },
  {
    path: "/auth",
    name: "auth",
    component: AuthView,
    beforeEnter: userAuth,
  },
  {
    path: "/verify-code",
    name: "verify-code",
    component: VerifyCodeView,
    beforeEnter: userAuth,
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

router.beforeEach(
  (
    // @ts-ignore
    to,
    // @ts-ignore
    from,
    next,
  ) => {
    getCookieAuth().then(() => {
      next();
    });
  },
);
export default router;
