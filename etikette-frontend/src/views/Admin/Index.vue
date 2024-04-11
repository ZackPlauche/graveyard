<template>
    <main class="admin flex bg-secondary">
        <sidebar>
            <router-link class="sidebar-link" :to="{ name: 'Dashboard' }">Home<i class="sidebar-link-icon fas fa-home"></i></router-link>
            <router-link class="sidebar-link" :class="{ active: $route.path.includes('menus') }" :to="{ name: 'MenuList' }">Menus<i class="sidebar-link-icon fas fa-book-open"></i></router-link>
            <router-link class="sidebar-link" :to="{ name: 'Settings' }">Settings<i class="sidebar-link-icon fas fa-cog"></i></router-link>
        </sidebar>
        <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
                <component class="w-100" :is="Component"></component>
            </transition>
        </router-view>
    </main>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'

export default {
    components: {
        Sidebar
    }
}

</script>
