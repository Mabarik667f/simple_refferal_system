<script lang="ts">
import { defineComponent } from "vue";
import {
    Profile,
    ListPhones,
    LogoutBtn,
    ActivateForm,
} from "@/modules/UserModule";
export default defineComponent({
    components: {
        Profile,
        ListPhones,
        LogoutBtn,
        ActivateForm,
    },
});
</script>

<template>
    <div class="container">
        <div class="left">
            <div>
                <Profile />
            </div>
            <div>
                <ActivateForm />
            </div>
        </div>
        <div class="right">
            <div>
                <LogoutBtn />
            </div>
            <div>
                <ListPhones />
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    justify-content: space-between;
    height: 500px;
}

.left {
    display: flex;
    flex-direction: column;
    width: 50%;
}

.right {
    display: flex;
    flex-direction: column;
    width: 50%;
}

.left div,
.right div {
    margin-bottom: 30px;
}
</style>
