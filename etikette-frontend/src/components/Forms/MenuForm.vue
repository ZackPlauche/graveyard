<template>
    <form @submit.prevent="onSubmit">
        <fieldset>
            <field type="text" name="title" v-model="menu.title" />
            <field type="textarea" name="description" v-model="menu.description" />
            <field type="file" name="image" v-model="menu.image" />
        </fieldset>
    </form>
</template>

<script>
import api from '@/api'

export default {
    name: 'MenuForm',
    setup(props) {
        const menu = ref({
            title: null,
            description: null,
            
        })

        return { menu }
    },
    props: {
        initialMenu: {
            type: Object,
            default() {
                return {}
            }
        }
    },
    data() {
        return {
            menu: this.initialMenu
        }
    },
    methods: {
        onSubmit() {
            console.log()
        }
    }
}
</script>