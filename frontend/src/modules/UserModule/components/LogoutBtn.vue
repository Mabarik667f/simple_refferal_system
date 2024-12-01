<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "@/store/authStore";
export default defineComponent({
    setup() {
        const store = authStore();
        const router = useRouter();
        const { clearCookies } = store;
        const logoutHook = () => {
            clearCookies();
            router.push("/auth");
        };
        return { logoutHook };
    },
});
</script>

<template>
    <c-button @click="logoutHook">Выйти</c-button>
</template>

<style scoped></style>
