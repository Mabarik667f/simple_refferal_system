import { defineStore } from "pinia";
import { ref } from "vue";
import Cookies from "js-cookie";

export const authStore = defineStore("auth", () => {
  const isAuth = ref<boolean>(false);
  const userId = ref<number>(0);
  const activatedCode = ref<string | null>(null);

  async function setIsAuth(flag: boolean) {
    isAuth.value = flag;
    Cookies.set("isAuth", flag.toString());
  }

  async function getCookieAuth() {
    isAuth.value = Cookies.get("isAuth") === "true";
  }

  async function setUserTemporaryData(phone: string, code: string) {
    Cookies.set("phone", phone);
    Cookies.set("code", code);
  }

  async function setUserData(user_pk: number, acCode: string | null) {
    userId.value = user_pk;
    activatedCode.value = acCode;
  }

  async function setToken(token: string) {
    Cookies.set("token", token);
    Cookies.remove("code");
  }

  async function clearCookies() {
    const allCookies = Cookies.get();

    for (const cookieName in allCookies) {
      if (allCookies.hasOwnProperty(cookieName)) {
        Cookies.remove(cookieName);
      }
    }
  }

  return {
    isAuth,
    userId,
    activatedCode,
    setIsAuth,
    getCookieAuth,
    setToken,
    setUserTemporaryData,
    setUserData,
    clearCookies,
  };
});
