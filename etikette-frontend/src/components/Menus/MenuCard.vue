<template>
    <router-link class="menu-card" :to="{ name: 'MenuDetail', params: { slug: menu.slug } }" >
        <img v-if="hasImage(menu)" :src="menu.image" class="menu-card-image">
        <div class="menu-card-body" :class="{ 'text-white': hasImage(menu)}" >
            <h2 class="menu-card-title">{{ menu.title }}</h2>
        </div>
    </router-link>
</template>

<script>

export default {
    name: 'MenuCard',
    props: { 
        menu: { 
            type: Object, 
            required: true 
        }
    },
    methods: {
        hasImage(menu) { return menu.image && menu.image.length > 0 }
    }
}
</script>

<style lang="scss">

.menu-card {
    display: block;
    text-decoration: none;
    color: var(--text-color);
    background-color: var(--primary-bg);
    height: 200px;
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
    border-radius: 15px;
    cursor: pointer;
    overflow: hidden;
    background-size: cover;
    background-position: center;
    position: relative;
    box-shadow: 0 2.5px 5px lightgrey;
    transition: box-shadow .4s ease;

    &:hover { box-shadow: 0 7.5px 15px lightgrey; }
    &:active { 
        transition: none;
        box-shadow: 0;
    }
}

.menu-card-body {
    position: relative;
    padding: 10px 15px;
    height: 100%;
    width: 100%;
    z-index: 1;
    transition: background-color .4s ease;

    @at-root .menu-card-image + & { background-color: #0004; }
}

.menu-card-image {
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    object-fit: cover;
    object-position: center;
    transition: transform .5s ease;
    will-change: transform;

    @at-root .menu-card:hover & { transform: scale(1.04); }
    @at-root .ghost .menu-card:active & { 
        transition: none;
        transform: scale(1);
    }
    @at-root .ghost .menu-card:hover & { 
        transition: none;
        transform: scale(1);
    }
}

</style>