<script lang="ts">
import Cookies from "js-cookie";
import { useRouter } from "vue-router";
import { defineComponent, ref, onMounted } from "vue";
import { authStore } from "@/store/authStore";
import { ErrorTypes } from "@/interfaces/errorIntefaces";
import verifyCode from "../api/verifyCode";
export default defineComponent({
    setup() {
        const router = useRouter();
        const store = authStore();
        const { setToken, setIsAuth } = store;

        const code = ref<string>("");
        const errors = ref<ErrorTypes>({
            code: "",
        });

        const verifyCodeHook = async () => {
            const response = await verifyCode(code.value);
            const result = await response.json();
            if (response.ok) {
                setToken(result["token"]);
                setIsAuth(true);
                router.push("home");
            } else {
                errors.value.code = "Неверный код";
                code.value = "";
            }
        };
        onMounted(() => alert(`Ваш код: ${Cookies.get("code")}`));
        return { code, verifyCodeHook, errors };
    },
});
</script>

<template>
    <c-form method="post" @submit.prevent="verifyCodeHook" class="code-form">
        <template v-slot:header>
            <h1>Проверка</h1>
        </template>
        <template v-slot:fields>
            <div class="lb-block">
                <cf-label :for="'code'">Код подтверждения </cf-label>
                <span class="error" v-for="error in errors.code">{{
                    error
                }}</span>
            </div>
            <div class="mb-4">
                <c-input
                    v-model="code"
                    :id="'code'"
                    :placeHolder="'Код в формате 0000'"
                    maxlength="4"
                    required
                />
            </div>
        </template>
        <template v-slot:footer>
            <c-button>Продолжить</c-button>
        </template>
    </c-form>
</template>

<style scoped>
.code-form {
    display: flex;
    flex-direction: column;
    background: orange;
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    color: #fff;
    width: 420px;
    height: 300px;
    padding: 30px 40px;
    border-radius: 10px;
    justify-content: space-between;
}

.cf-label .error {
    display: inline-block;
    word-wrap: nowrap;
    white-space: nowrap;
}

.lb-block {
    display: flex;
    justify-content: space-around;
}
</style>
