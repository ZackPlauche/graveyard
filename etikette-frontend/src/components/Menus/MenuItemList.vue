<template>
    <ol class="menu-item-list">
        <li v-for="menuItem in menuItems" :key="menuItem.id">
            <MenuItem :menu-item="menuItem" />
        </li>
    </ol>
</template>

<script>
import MenuItem from './MenuItem.vue'

export default {
    name: 'MenuItemList',
    components: { MenuItem },
    props: { 
        menuItems: { 
            type: Array, 
            required: true 
        }
    }
}
</script>


<style>

.menu-item-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    justify-content: center;
    gap: 20px;
    list-style: none;
}

</style>