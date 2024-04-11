<template>
    <div class="menu-item">
        <img :src="menuItem.image" alt="" class="menu-item-image">
        <div class="menu-item-title">{{ menuItem.title }}</div>
        <div class="menu-item-description">{{ menuItem.description }}</div>
        <div class="menu-item-price">${{ menuItem.price }}</div>
    </div>
</template>

<script>

export default {
    name: 'MenuItem',
    props: {
        menuItem: {
            type: Object,
            required: true,
        }
    }
}

</script>

<style lang="scss">
    .menu-item {
        padding: 10px;
        background-color: var(--primary-bg);
        box-shadow: 0 1.25px 5px lightgrey;
        border-radius: 10px;
        overflow: hidden;

        &-image {
            display: block;
            height: 200px;
            width: 100%;
            object-fit: cover;
            object-position: center;
            margin-bottom: 10px;
        }

        &-title {
            font-weight: 500;
            font-size: 18px;
            margin-bottom: 5px;
        }
    }
</style>