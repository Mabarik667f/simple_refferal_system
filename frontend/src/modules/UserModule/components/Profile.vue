<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { IUser } from "../interfaces";
import { authStore } from "@/store/authStore";
import getMe from "../api/getMe";
export default defineComponent({
    setup() {
        const store = authStore();
        const userData = ref<IUser>({
            id: 0,
            phone: "",
            my_code: "",
            activated_code: "",
        });

        const { setUserData } = store;
        onMounted(async () => {
            userData.value = await getMe();
            setUserData(userData.value.id, userData.value.activated_code);
        });
        return { userData };
    },
});
</script>

<template>
    <div class="profile-container">
        <h1>Профиль</h1>
        <div class="profile-item">
            <cf-label :for="'id'">Id:</cf-label>
            <div class="item-text" :id="'id'">{{ userData.id }}</div>
        </div>
        <div class="profile-item">
            <cf-label :for="'phone'">Телефон:</cf-label>
            <div class="item-text" :id="'phone'">{{ userData.phone }}</div>
        </div>
        <div class="profile-item">
            <cf-label :for="'code'">Мой код:</cf-label>
            <div class="item-text" :id="'code'">{{ userData.my_code }}</div>
        </div>
    </div>
</template>

<style scoped>
.profile-container {
    width: 350px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 10px;
}

.profile-container h1 {
    text-align: center;
    margin-bottom: 20px;
}
.profile-item {
    font-size: 18px;
    margin-bottom: 10px;
    display: flex;
}

.profile-item strong {
    color: #333;
}

.item-text {
    margin-left: 15px;
}
</style>
