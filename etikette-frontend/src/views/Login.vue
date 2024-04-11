<template>
    <main class="login container py-3">
            <h1 class="text-center mb-2">Login</h1>
            <LoginForm class="mx-auto" style="max-width: 400px"/>
    </main>
</template>

<script>
import LoginForm from '@/components/Forms/LoginForm.vue'

export default {
    components: {
        LoginForm
    }
}
</script>