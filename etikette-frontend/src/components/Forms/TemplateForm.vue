<template>
    <form>
        <slot>
            <fieldset>
                <field 
                    v-for="(value, key, index) in templateObject" 
                    :key="index" 
                    :type="determineFormType(value, key)"
                    />
            </fieldset>
        </slot>
        <BaseButton type="submit">{{ cta }}</BaseButton>
    </form>
</template>

<script>
// TODO: This whole component might be extra
import { BaseButton } from '@/components/Buttons'

export default {
    components: {
        BaseButton,
    },
    props: {
        templateObject: { 
            type: Object,
            required: true,
        },
        cta: {
            type: String,
            default: 'Action',
        }
    },
    methods: {
        determineFormType(value, key) {
            switch (key) {
                case 'password': 
                    return 'password'
                case 'color':
                    return 'color'
            }

            switch (typeof value) {            
                case 'string':
                    return 'text'
                case 'number':
                    return 'number'
            }
        }
    }

}

</script>