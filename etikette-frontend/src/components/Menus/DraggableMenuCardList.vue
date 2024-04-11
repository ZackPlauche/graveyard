<template>
    <draggable v-bind="draggableProps" tag="transition-group" :component-data="transitionGroupData">
        <template #item="{element}">
            <li :key="element.id">
                <MenuCard :style="{ cursor: $attrs.disabled ? 'pointer': 'grab' }" :menu="element"/>
            </li>
        </template>
    </draggable>
</template>

<script>
import MenuCard from './MenuCard.vue'
import draggable from 'vuedraggable'
import { ref } from 'vue'

export default {
    components: {
        MenuCard,
        draggable,
    },
    setup() {
        const draggableProps = {
            ghostClass: 'ghost',
            animation: 200,
            tag: "transition-group",
            itemKey: "id",
        }
        const transitionGroupData = { 
            name: 'flip-list', 
            tag: 'ul', 
            class: 'menu-card-list pb-2'
        }
        return { draggableProps, transitionGroupData }
    },
}
</script>