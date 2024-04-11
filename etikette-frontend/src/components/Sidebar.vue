<template>
        <div class="sidebar" :class="{ 'sidebar-is-closed': !sidebarOpen }">
            <slot></slot>
        </div>
        <teleport to=".navbar">
            <button class="sidebar-toggle" :class="{ closed: !sidebarOpen }" @click="sidebarOpen = !sidebarOpen">
                <i class="sidebar-toggle-icon fas fa-ellipsis-h"></i>
            </button>
        </teleport>
</template>

<script>
export default {
    data() {
        return {
            sidebarOpen: true,
        }
    }
}
</script>

<style lang="scss">
    :root {
        --sidebar-width: 260px;
        --sidebar-close-size: 50px;
    }

    .sidebar {
        background-color: var(--primary-bg);
        min-width: var(--sidebar-width);
        width: var(--sidebar-width);
        min-height: calc(100vh - var(--navbar-height));
        top: var(--navbar-height);
        position: sticky;
        align-self: flex-start;
        transition: margin .5s ease;
        overflow: hidden;

        &-is-closed {margin-left: calc(-1 * calc(var(--sidebar-width) - var(--sidebar-close-size)))}

        @media screen and (max-width: 600px) {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            justify-items: center;
            position: fixed;
            height: var(--sidebar-close-size);
            min-height: var(--sidebar-close-size);
            width: 100%;
            min-width: 100%;
            top: auto;
            bottom: 0;
            right: 0;
            left: 0;
            margin: 0;
            z-index: 9;
            box-shadow: 0 0 5px lightgrey;

            .sidebar-link { 
                font-size: 0;
                width: 100%;
             }
            .sidebar-link-icon { width: 100%}
        }
    }

    .sidebar-toggle {
        display: flex;
        height: 40px;
        width: 40px;
        justify-content: center;
        align-items: center;
        position: absolute;
        background-color: var(--primary-bg);
        top: calc(.5 * var(--navbar-height));
        transform: translateY(-50%);
        left: 5px;
        cursor: pointer;
        transition: background-color .3s ease;
        border-radius: 5px;
        user-select: none;
        animation: fade-in .4s ease;

        &:hover {
            background-color: var(--secondary-bg);
        }

        @media screen and (max-width: 600px) {
            display: none;
        }
    }

    .sidebar-toggle-icon {
        display: block;
        transition: transform .5s ease;
        font-size: 22px;
        user-select: none;
        @at-root .sidebar-toggle.closed & { transform: rotate(90deg); }
    }

    .sidebar-link {
        display: flex;
        align-items: center;
        padding: 0 20px;
        text-decoration: none;
        font-size: 20px;
        height: var(--sidebar-close-size);
        color: var(--text-color);
        transition: color .2s ease, background-color .2s ease;
        position: relative;

        &.active,
        &:hover {
            color: var(--primary);
        }

        &.active {
            background-color: var(--secondary-bg);
        }
    }

    .sidebar-link-icon {
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        right: 0;
        font-size: 22px;
        color: lightgrey;
        height: var(--sidebar-close-size);
        width: var(--sidebar-close-size);
        transition: color .2s ease, background-color .2s ease;

        @at-root .sidebar-link.active & {
            color: var(--primary);
        }

        @at-root .sidebar-link:hover & {
            color: var(--primary);
        }

        @at-root .theme-dark & {
            color: var(--text-color);
        }

    }

</style>