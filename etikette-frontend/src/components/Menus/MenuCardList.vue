<template>
    <ol class="menu-card-list">
        <li v-for="menu in menus" :key="menu.id">
            <MenuCard :menu="menu" />
        </li>
    </ol>
</template>

<script>
import MenuCard from './MenuCard.vue'

export default {
    name: 'MenuCardList',
    components: { MenuCard },
    props: {
        menus: {
            type: Array,
            required: true
        }
    }

}

</script>