<template>
    <div class="menus relative">
        <div class="container pt-2 pb-5">
            <h1 class="text-center mb-2">Menus</h1>
            <ButtonList class="mb-2" gap="15px">
                <BaseButton class="btn-success">Add Menu <i class="fas fa-plus"></i></BaseButton>
                <EditButton 
                    :edit-mode="editMode"
                    @click="editButtonClick"
                    >
                    <span v-if="!editMode">Edit Menu Order </span>
                    <span v-else>Cancel </span>
                    <i class="fas" :class="!editMode ? 'fa-pencil' : 'fa-times'"></i>
                </EditButton>
                <SaveButton v-if="editMode" :disabled="!contentEdited" @click="save" />
            </ButtonList>
            <DraggableMenuCardList v-model="menus" :disabled="!editMode" @change="updateOrder" />
        </div>
    </div>
</template>

<script>
import { DraggableMenuCardList } from '@/components/Menus'
import api from '@/api'
import { objectsAreSame } from '@/utils/objects.js'
import { ButtonList, SaveButton, EditButton, BaseButton } from '@/components/Buttons'
import { updateAllObjectsOrder, updateMovedObject } from '@/utils/sortable.js'

export default {
    name: 'MenuList',
    components: {
        DraggableMenuCardList,
        ButtonList,
        BaseButton,
        SaveButton,
        EditButton,
    },
    data() { 
        return {
            editMode: false,
            contentEdited: false,
            menus: [],
        }
    },
    async mounted() {
        this.menus = await api.get('menus')
    },
    watch: {
        menus(beforeMenus, afterMenus) {
            if (!(afterMenus[0])) {
                this.initialMenuState = beforeMenus
            } else {
                this.contentEdited = objectsAreSame(afterMenus, this.initialMenuState)
            }
        }
    },
    methods: {
        updateOrder({ moved }) {
            let movedMenu = updateMovedObject(moved, this.menus)
            updateAllObjectsOrder(moved, this.menus, movedMenu)
        },
        save() {
            this.menus.forEach(menu => {
                api.patch('menus', menu.slug, { order: menu.order })
            })
            this.editMode = false
            this.contentEdited = false
            this.initialMenuState = this.menus
        },
        resetMenus() {
            this.menus = this.initialMenuState
            this.contentEdited = false
        },
        editButtonClick() {
            if (!this.editMode) {
                this.editMode = true
            } else {
                this.resetMenus()
                this.editMode = false
            }
        }
    }
}

</script>

<style lang="scss">

.menu-card-list {
    display: flex;
    flex-flow: column;
    list-style: none;
    gap: 25px;
}

</style>