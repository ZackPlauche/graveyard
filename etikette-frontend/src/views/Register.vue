<template>
    <main class="signup-page container py-3">
        <h1 class="text-center mb-3">Register</h1>
        <RegisterForm class="mx-auto" style="max-width: 400px;" />
    </main>
</template>

<script>
import RegisterForm from '@/components/Forms/RegisterForm.vue'

export default {
    components: {
        RegisterForm
    }
}
</script>