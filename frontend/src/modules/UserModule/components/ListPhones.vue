<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import getList from "../api/getList";
export default defineComponent({
    setup() {
        const phones = ref<Array<string>>([]);
        onMounted(async () => {
            phones.value = await getList();
        });
        return { phones };
    },
});
</script>

<template>
    <div>
        <h4>Список номеров пользователей, активировавших ваш код:</h4>
        <ul>
            <li v-for="phone in phones" :key="phone">
                {{ phone }}
            </li>
        </ul>
    </div>
</template>

<style scoped>
li {
    list-style: none;
    font-size: 18px;
}
</style>
