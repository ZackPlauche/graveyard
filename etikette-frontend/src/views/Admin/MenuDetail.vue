<template>
    <div class="menu-detail">
        <Menu :menu="menu"></Menu>
    </div>
</template>

<script>
import { Menu } from '@/components/Menus'
import api from '@/api'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
    components: { 
        Menu,
    },
    setup() {
        const menu = ref({})
        const menuSlug = useRoute().params.slug
        onMounted(async () => menu.value = await api.getSpecific('menus', menuSlug))
        return { menu }
    },
}
</script>
