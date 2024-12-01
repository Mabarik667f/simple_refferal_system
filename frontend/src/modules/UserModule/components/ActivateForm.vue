<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { ErrorTypes } from "@/interfaces/errorIntefaces";
import activateInvitationCode from "../api/activateInvitationCode";
import { storeToRefs } from "pinia";
import { authStore } from "@/store/authStore";
export default defineComponent({
    setup() {
        const store = authStore();
        const { activatedCode } = storeToRefs(store);
        const code = ref<string>(activatedCode.value || "");

        watch(activatedCode, (newCode) => {
            if (newCode !== null) {
                code.value = newCode;
            } else {
                code.value = "";
            }
        });
        const errors = ref<ErrorTypes>({
            invitation_code: "",
        });

        const activateCodeHook = async () => {
            const response = await activateInvitationCode(code.value);
            if (response.ok) {
                activatedCode.value = code.value;
                alert("Активация кода прошла успешно!");
            } else {
                const result = await response.json();
                errors.value = result;
                code.value = "";
            }
        };
        return { code, activateCodeHook, activatedCode, errors };
    },
});
</script>

<template>
    <c-form method="post" @submit.prevent="activateCodeHook">
        <template v-slot:fields>
            <div class="lb-block">
                <cf-label :for="'code'"><h5>Инвайт код</h5> </cf-label>
                <span class="error" v-for="error in errors.invitation_code">{{
                    error
                }}</span>
            </div>
            <div class="mb-4">
                <c-input
                    v-model="code"
                    :id="'code'"
                    :placeHolder="'Код в формате Abc123'"
                    minlength="6"
                    maxlength="6"
                    :disabled="activatedCode !== null"
                    required
                />
            </div>
        </template>
        <template v-slot:footer>
            <c-button :disabled="activatedCode !== null">Активировать</c-button>
        </template>
    </c-form>
</template>

<style scoped>
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
