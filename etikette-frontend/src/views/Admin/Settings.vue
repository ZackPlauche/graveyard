<template>
    <div class="settings">
        <div class="container py-2">
            <div class="relative">
                <h1 class="text-center mb-2">Settings</h1>
                <form class="mx-auto" style="width: 400px" @submit.prevent="onSubmit">
                    <field type="file" name="image" v-model="settings.image" />
                    <field type="text" name="credit_name" v-model="settings.creditName" />
                    <field type="number" name="price_per_credit" step="0.01" min="0" v-model="settings.pricePerCredit" />
                    <button :class="['btn btn-primary absolute top right', { disabled: !changesMade }]" type="submit" :disabled="!changesMade">Save</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
    setup() {
        const settings = ref({
            image: '',
            creditName: 'Credits',
            pricePerCredit: 9.99
        })

        const initialState = Object(settings.value)
        const changesMade = ref(false)

        watch([settings.value], ([beforeSettings], [afterSettings]) => {
            console.log(settings.value)
            console.log(initialState)
            changesMade.value = true
        })

        return { changesMade, settings }
    }
}


</script>