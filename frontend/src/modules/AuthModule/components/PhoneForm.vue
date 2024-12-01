<script lang="ts">
import { useRouter } from "vue-router";
import { defineComponent, ref } from "vue";
import { authStore } from "@/store/authStore";
import { ErrorTypes } from "@/interfaces/errorIntefaces";
import auth from "../api/auth";
export default defineComponent({
    setup() {
        const router = useRouter();
        const store = authStore();
        const { setUserTemporaryData } = store;

        const phone = ref<string>("");
        const errors = ref<ErrorTypes>({
            phone: "",
        });

        const authHook = async () => {
            const result = await auth(phone.value);
            if (Object.keys(result).length >= 2) {
                setUserTemporaryData(result["phone"], result["code"]);
                router.push("verify-code");
            } else {
                errors.value = result;
                phone.value = "";
            }
        };
        return { phone, authHook, errors };
    },
});
</script>

<template>
    <c-form method="post" @submit.prevent="authHook" class="phone-form">
        <template v-slot:header>
            <h1>Войти</h1>
        </template>
        <template v-slot:fields>
            <div class="lb-block">
                <cf-label :for="'phone'">Номер телефона </cf-label>
                <span class="error" v-for="error in errors.phone">{{
                    error
                }}</span>
            </div>
            <div class="mb-4">
                <c-input
                    v-model="phone"
                    :id="'phone'"
                    :placeHolder="'Номер в формате 70123456789'"
                    maxlength="11"
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
.phone-form {
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

.pass-errors {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin-top: 5px;
    margin-left: 10px;
}

.cf-label .error {
    display: block;
    margin-top: 5px;
    word-wrap: break-word;
    white-space: normal;
}

.lb-block {
    display: flex;
    justify-content: space-between;
}
</style>
