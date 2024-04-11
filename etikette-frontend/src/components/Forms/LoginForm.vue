<template>
   <form class="login-form" method="POST" @submit.prevent="onSubmit">
            <fieldset>
                <field type="text" name="username" autocomplete="username" v-model="username" />
                <field type="password" name="password" autocomplete="password" v-model="password" />
            </fieldset>
            <button class="btn btn-primary w-100" type="submit">Login</button>
   </form>
</template>

<script>


export default {
    name: 'LoginForm',
    data() {
        return {
            username: null,
            password: null,
        }
    },
    methods: {
        onSubmit() {
            const userInfo = {
                username: this.username,
                password: this.password,
            }
            if (this.validate(userInfo)) {
                this.$router.push({ name: 'Dashboard'})
            }
        },
        validate(userInfo) {
            return userInfo.username && userInfo.password
        }
    }
}
</script>

<style>
.btn-form {
    color: white;
    background-color: var(--primary);
    font-size: 18px;
    width: 100%;
    border-radius: 5px;
    margin-top: 5px;
}
</style>