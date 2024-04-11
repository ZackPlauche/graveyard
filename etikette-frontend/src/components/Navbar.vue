<template>
    <nav class="navbar">
        <div class="navbar-nav">
            <router-link :to="{ name: 'Home' }" class="navbar-logo">etikëtte</router-link>
            <div v-if="mobileMenuIconShow" @click="mobileMenuOpen = true" class="mobile-menu-icon">
                <div class="mobile-menu-icon-bar"></div>
            </div>
            <div :class="[mobileMenuIconShow ? 'mobile-menu' : 'navbar-menu']">
                    <slot></slot>
            </div>
        </div>
    </nav>
</template>

<script>

export default {
    data() {
        return {
            mobileMenuOpen: false,
            mobileMenuIconShow: false,
        }
    }
}
</script>

<style lang="scss">

:root {
    --navbar-height: 80px;
}

.navbar {
    height: var(--navbar-height);
    background-color: var(--primary-bg);
    box-shadow: 0 0 1px grey;
}

.navbar-nav {
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
}

.navbar-logo {
    text-decoration: none;
    font-size: calc(var(--navbar-height) * .6);
    font-family: var(--display-font);
    color: var(--text-color);
    padding: 0;
    margin: 0;
    transition: color .2s ease;
    position: absolute;
    left: 60px;
    z-index: 1;
    
    &:hover {color: var(--primary)}
}

.navbar-menu,
.nav-link-list {
    display: flex;
    align-items: center;
    gap: 15px;
    list-style: none;
    position: absolute;
    right: 25px;
}

.mobile-menu {
    display: none;
    flex-flow: column;
    gap: 20px;
    justify-content: center;
    align-items: center;
    list-style: none;
}

.nav-link {
    text-decoration: none;
    transition: color .2s ease;
    color: var(--text-color);
    font-size: 18px;
    white-space: nowrap;

    &:hover,
    &.active {color: var(--primary)}
}

</style>