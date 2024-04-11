<template>
    <div class="menu">
        <hero :image="menu.image" class="text-white overlay overlay-dark overlay-5" style="min-height: 250px;">
            <h1>{{ menu.title }}</h1>
        </hero>
        <div class="container pt-3 pb-5">
            <MenuItemList v-if="hasItems(menu)" :menu-items="menu.items" />
            <p v-else>No items to display.</p>
        </div>
    </div>
</template>

<script>
import MenuItemList from './MenuItemList.vue'

export default {
    name: 'Menu',
    components: { MenuItemList },
    props: {
        menu: {
            type: Object,
            required: true,
        }
    },
    methods: {
        hasItems(menu) {
            return menu.items && menu.items.length > 0
        }
    }
}
</script>