<template>
    <form method="post" @submit.prevent="onSubmit">
        <fieldset>
            <field type="email" name="email" v-model="email" />
            <field type="text" name="first_name" v-model="firstName" />
            <field type="text" name="last_name" v-model="lastName" />
            <field type="password" name="password" v-model="password" />
            <field type="password" name="password2" label="Confirm Password" v-model="password2" />
        </fieldset>
        <button class="btn btn-primary w-100" type="submit">Sign Up</button>
    </form>
</template>

<script>
export default {
    name: 'RegisterForm',
    data() {
        return {
           firstName: null,
           lastName: null,
           email: null,
           password: null,
           password2: null, 
        }
    },
    methods: {
        onSubmit() {
            if (this.firstName && this.lastName && this.email && this.password && this.password2) {
                router.push({ name: 'Login' })
            }
        }
    }
}

</script>